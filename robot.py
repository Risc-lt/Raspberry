#!/usr/bin/env python3
"""
攀爬机器人控制类 - 修正版本
"""

import time
import RPi.GPIO as GPIO
from simple_pid import PID
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ClimbingRobot:
    def __init__(self):
        # GPIO设置
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # 引脚定义 (您可以根据实际接线修改)
        # 径向伸缩杆 (用于抓紧柱子)
        self.upper_radial_extend_pin = 18  # 上方径向伸缩杆伸长引脚
        self.upper_radial_retract_pin = 19  # 上方径向伸缩杆收缩引脚
        self.lower_radial_extend_pin = 20  # 下方径向伸缩杆伸长引脚:38->2
        self.lower_radial_retract_pin = 21  # 下方径向伸缩杆收缩引脚:40->1

        # 水平伸缩杆 (用于移动竖直杆位置)
        self.upper_horizontal_extend_pin = 22  # 上方水平伸缩杆伸长引脚
        self.upper_horizontal_retract_pin = 23  # 上方水平伸缩杆收缩引脚
        self.lower_horizontal_extend_pin = 24  # 下方水平伸缩杆伸长引脚
        self.lower_horizontal_retract_pin = 25  # 下方水平伸缩杆收缩引脚

        # 舵机
        self.upper_servo_pin = 12  # 上方舵机引脚
        self.lower_servo_pin = 13  # 下方舵机引脚

        # 竖直伸缩杆 - 双继电器控制
        self.vertical_extend_pin = 26  # 竖直伸缩杆伸长继电器引脚:36->4
        self.vertical_retract_pin = 16  # 竖直伸缩杆收缩继电器引脚:37->3

        # 超声波传感器 (HC-SR04)
        self.ultrasonic_trig_pin = 27  # 超声波触发引脚
        self.ultrasonic_echo_pin = 17  # 超声波回声引脚

        # 舵机参数 - 必须在setup_gpio()之前定义
        self.servo_frequency = 50  # 舵机PWM频率
        self.servo_neutral_duty = 7.5  # 中性位置占空比
        self.servo_degree_ratio = 18.0  # 角度转换比例

        # 时间参数 (秒) - 为每种杆设置独立的时间
        # 30cm直径柱子的收缩时间
        self.radial_retract_time_30cm = 3.0  # 径向杆收缩时间
        self.horizontal_retract_time_30cm = 1.5  # 水平杆收缩时间 

        # 60cm直径柱子的收缩时间
        self.radial_retract_time_60cm = 10.0  # 径向杆收缩时间 
        self.horizontal_retract_time_60cm = 1.0  # 水平杆收缩时间 

        # 攀爬时的时间参数
        self.extend_time = 3.0  # 径向杆伸长5cm所需时间 
        self.vertical_extend_time = 3.0  # 竖直杆伸长时间 
        self.servo_rotation_time = 0.5  # 舵机旋转时间 

        # 最终松开时间参数
        self.final_extend_time_rad = 20.0  # 最终伸长时间（秒）
        self.final_extend_time_hor = 6.0  # 最终伸长时间（秒）

        # 系统参数
        self.height_tolerance = 2.0  # 高度容忍度 (cm)

        # 柱子直径配置
        self.column_diameter_30cm = 30.0  # 30cm直径柱子
        self.column_diameter_60cm = 60.0  # 60cm直径柱子

        # 超声波参数
        self.sound_speed = 34300  # 声速 cm/s
        self.ultrasonic_timeout = 0.1  # 超声波测量超时时间

        # 初始化GPIO - 现在所有参数都已经定义了
        self.setup_gpio()

        # 机器人状态
        self.is_climbing = False

    def setup_gpio(self):
        """初始化GPIO引脚"""
        # 设置径向伸缩杆控制引脚为输出
        GPIO.setup(self.upper_radial_extend_pin, GPIO.OUT)
        GPIO.setup(self.upper_radial_retract_pin, GPIO.OUT)
        GPIO.setup(self.lower_radial_extend_pin, GPIO.OUT)
        GPIO.setup(self.lower_radial_retract_pin, GPIO.OUT)

        # 设置水平伸缩杆控制引脚为输出
        GPIO.setup(self.upper_horizontal_extend_pin, GPIO.OUT)
        GPIO.setup(self.upper_horizontal_retract_pin, GPIO.OUT)
        GPIO.setup(self.lower_horizontal_extend_pin, GPIO.OUT)
        GPIO.setup(self.lower_horizontal_retract_pin, GPIO.OUT)

        # 设置竖直伸缩杆控制引脚为输出
        GPIO.setup(self.vertical_extend_pin, GPIO.OUT)
        GPIO.setup(self.vertical_retract_pin, GPIO.OUT)

        # 设置超声波传感器引脚
        GPIO.setup(self.ultrasonic_trig_pin, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin, GPIO.IN)

        # 设置舵机引脚为PWM输出
        GPIO.setup(self.upper_servo_pin, GPIO.OUT)
        GPIO.setup(self.lower_servo_pin, GPIO.OUT)

        # 初始化PWM - 现在servo_frequency已经定义了
        self.upper_servo = GPIO.PWM(self.upper_servo_pin, self.servo_frequency)
        self.lower_servo = GPIO.PWM(self.lower_servo_pin, self.servo_frequency)
        self.upper_servo.start(self.servo_neutral_duty)
        self.lower_servo.start(self.servo_neutral_duty)

        # 初始状态设为低电平
        GPIO.output(self.upper_radial_extend_pin, GPIO.LOW)
        GPIO.output(self.upper_radial_retract_pin, GPIO.LOW)
        GPIO.output(self.lower_radial_extend_pin, GPIO.LOW)
        GPIO.output(self.lower_radial_retract_pin, GPIO.LOW)
        GPIO.output(self.upper_horizontal_extend_pin, GPIO.LOW)
        GPIO.output(self.upper_horizontal_retract_pin, GPIO.LOW)
        GPIO.output(self.lower_horizontal_extend_pin, GPIO.LOW)
        GPIO.output(self.lower_horizontal_retract_pin, GPIO.LOW)
        GPIO.output(self.vertical_extend_pin, GPIO.LOW)
        GPIO.output(self.vertical_retract_pin, GPIO.LOW)

        # 初始化超声波传感器
        GPIO.output(self.ultrasonic_trig_pin, GPIO.LOW)
        time.sleep(0.1)  # 让传感器稳定

    def get_current_height(self):
        """
        使用HC-SR04超声波传感器获取当前距离
        返回: 当前检测距离 (cm)
        """
        try:
            # 发送10微秒的触发信号
            GPIO.output(self.ultrasonic_trig_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.ultrasonic_trig_pin, GPIO.LOW)
            
            # 记录发送超声波的时刻
            while GPIO.input(self.ultrasonic_echo_pin) == 0:
                pulse_start = time.time()
            
            # 记录接收到回声的时刻
            while GPIO.input(self.ultrasonic_echo_pin) == 1:
                pulse_end = time.time()
            
            # 计算超声波往返时间
            pulse_duration = pulse_end - pulse_start
            
            # 计算距离（声速34300cm/s，往返需除以2）
            distance = pulse_duration * 34300 / 2
            
            return round(distance, 2)

        except Exception as e:
            logger.error(f"超声波距离测量异常: {e}")
            return 0.0

    # 径向伸缩杆控制函数 - 双继电器控制
    def control_upper_radial_extend(self, duration):
        """控制上方径向伸缩杆伸长 - 双继电器控制"""
        logger.info(f"上方径向伸缩杆伸长 {duration}秒")
        # 确保收缩继电器断开
        GPIO.output(self.upper_radial_retract_pin, GPIO.LOW)
        # 激活伸长继电器
        GPIO.output(self.upper_radial_extend_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.upper_radial_extend_pin, GPIO.LOW)

    def control_upper_radial_retract(self, duration):
        """控制上方径向伸缩杆收缩 - 双继电器控制"""
        logger.info(f"上方径向伸缩杆收缩 {duration}秒")
        # 确保伸长继电器断开
        GPIO.output(self.upper_radial_extend_pin, GPIO.LOW)
        # 激活收缩继电器
        GPIO.output(self.upper_radial_retract_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.upper_radial_retract_pin, GPIO.LOW)

    def control_lower_radial_extend(self, duration):
        """控制下方径向伸缩杆伸长 - 双继电器控制"""
        logger.info(f"下方径向伸缩杆伸长 {duration}秒")
        # 确保收缩继电器断开
        GPIO.output(self.lower_radial_retract_pin, GPIO.LOW)
        # 激活伸长继电器
        GPIO.output(self.lower_radial_extend_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.lower_radial_extend_pin, GPIO.LOW)

    def control_lower_radial_retract(self, duration):
        """控制下方径向伸缩杆收缩 - 双继电器控制"""
        logger.info(f"下方径向伸缩杆收缩 {duration}秒")
        # 确保伸长继电器断开
        GPIO.output(self.lower_radial_extend_pin, GPIO.LOW)
        # 激活收缩继电器
        GPIO.output(self.lower_radial_retract_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.lower_radial_retract_pin, GPIO.LOW)

    # 水平伸缩杆控制函数
    def control_upper_horizontal_extend(self, duration):
        """控制上方水平伸缩杆伸长"""
        logger.info(f"上方水平伸缩杆伸长 {duration}秒")
        GPIO.output(self.upper_horizontal_extend_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.upper_horizontal_extend_pin, GPIO.LOW)

    def control_upper_horizontal_retract(self, duration):
        """控制上方水平伸缩杆收缩"""
        logger.info(f"上方水平伸缩杆收缩 {duration}秒")
        GPIO.output(self.upper_horizontal_retract_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.upper_horizontal_retract_pin, GPIO.LOW)

    # 红3黑4为先伸长后缩短
    def control_lower_horizontal_extend(self, duration):
        """控制下方水平伸缩杆伸长"""
        logger.info(f"下方水平伸缩杆伸长 {duration}秒")
        GPIO.output(self.lower_horizontal_extend_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.lower_horizontal_extend_pin, GPIO.LOW)

    def control_lower_horizontal_retract(self, duration):
        """控制下方水平伸缩杆收缩"""
        logger.info(f"下方水平伸缩杆收缩 {duration}秒")
        GPIO.output(self.lower_horizontal_retract_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.lower_horizontal_retract_pin, GPIO.LOW)

    # 竖直伸缩杆控制函数 - 修改为双继电器控制
    def control_vertical_extend(self, duration):
        """控制竖直伸缩杆伸长 - 双继电器控制"""
        logger.info(f"竖直伸缩杆伸长 {duration}秒")
        # 确保收缩继电器断开
        GPIO.output(self.vertical_retract_pin, GPIO.LOW)
        # 激活伸长继电器
        GPIO.output(self.vertical_extend_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.vertical_extend_pin, GPIO.LOW)

    def control_vertical_retract(self, duration):
        """控制竖直伸缩杆收缩 - 双继电器控制"""
        logger.info(f"竖直伸缩杆收缩 {duration}秒")
        # 确保伸长继电器断开
        GPIO.output(self.vertical_extend_pin, GPIO.LOW)
        # 激活收缩继电器
        GPIO.output(self.vertical_retract_pin, GPIO.HIGH)
        time.sleep(duration)
        # 断电 - 两个继电器都设为低电平
        GPIO.output(self.vertical_retract_pin, GPIO.LOW)

    # 舵机控制函数 - 使用测试代码中的精确控制方式
    def rotate_upper_servo_ccw(self, degrees=5):
        """上方舵机逆时针旋转（杆向后）"""
        logger.info(f"上方舵机逆时针旋转 {degrees}度")
        duty_cycle = self.servo_neutral_duty - (degrees / self.servo_degree_ratio)
        self.upper_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(self.servo_rotation_time)

    def rotate_upper_servo_cw(self, degrees=5):
        """上方舵机顺时针旋转（杆向前）"""
        logger.info(f"上方舵机顺时针旋转 {degrees}度")
        duty_cycle = self.servo_neutral_duty + (degrees / self.servo_degree_ratio)
        self.upper_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(self.servo_rotation_time)

    def rotate_lower_servo_ccw(self, degrees=5):
        """下方舵机逆时针旋转（杆向后）"""
        logger.info(f"下方舵机逆时针旋转 {degrees}度")
        duty_cycle = self.servo_neutral_duty - (degrees / self.servo_degree_ratio)
        self.lower_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(self.servo_rotation_time)

    def rotate_lower_servo_cw(self, degrees=5):
        """下方舵机顺时针旋转（杆向前）"""
        logger.info(f"下方舵机顺时针旋转 {degrees}度")
        duty_cycle = self.servo_neutral_duty + (degrees / self.servo_degree_ratio)
        self.lower_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(self.servo_rotation_time)

    def reset_servos(self):
        """重置舵机到中性位置"""
        logger.info("重置舵机到中性位置")
        self.upper_servo.ChangeDutyCycle(self.servo_neutral_duty)
        self.lower_servo.ChangeDutyCycle(self.servo_neutral_duty)
        time.sleep(self.servo_rotation_time)

    def final_extend(self):
        """
        最终松开功能 - 伸长上下两个径向杆来松开对柱子的抓握，并收回水平杆
        """
        logger.info("=== 开始最终松开操作 ===")
        
        try:
            # 第一步：伸长上下径向杆松开柱子
            logger.info("伸长上下径向杆松开柱子...")
            self.control_upper_radial_extend(self.final_extend_time_rad)
            self.control_upper_horizontal_retract(self.final_extend_time_hor)
            
            logger.info("径向杆伸长完成，开始收回水平杆...")
            
            # 第二步：收回上下水平杆
            logger.info("收回上下水平杆...")
            self.control_lower_radial_extend(self.final_extend_time_rad)
            self.control_lower_horizontal_retract(self.final_extend_time_hor)
            
            logger.info("最终松开操作完成 - 机器人已松开柱子并收回水平杆")
            
        except Exception as e:
            logger.error(f"最终松开操作中出错: {e}")
            raise

    # 初始收缩函数
    def initial_retraction_30cm(self):
        """针对30cm直径柱子的初始收缩"""
        logger.info("开始30cm直径柱子初始收缩...")

        # 使用已有的控制函数，分别控制径向杆和水平杆
        logger.info("开始收缩径向伸缩杆...")
        self.control_upper_radial_retract(self.radial_retract_time_30cm)
        self.control_lower_radial_retract(self.radial_retract_time_30cm)

        # logger.info("径向杆收缩完成，开始收缩水平杆...")
        # self.control_upper_horizontal_retract(self.horizontal_retract_time_30cm)
        # self.control_lower_horizontal_retract(self.horizontal_retract_time_30cm)

        logger.info("30cm直径柱子初始收缩完成")

    def initial_retraction_60cm(self):
        """针对60cm直径柱子的初始收缩"""
        logger.info("开始60cm直径柱子初始收缩...")

        # 使用已有的控制函数，分别控制径向杆和水平杆
        logger.info("开始收缩径向伸缩杆...")
        self.control_upper_radial_retract(self.radial_retract_time_60cm)
        self.control_lower_radial_retract(self.radial_retract_time_60cm)

        logger.info("径向杆收缩完成，开始收缩水平杆...")
        self.control_upper_horizontal_retract(self.horizontal_retract_time_60cm)
        self.control_lower_horizontal_retract(self.horizontal_retract_time_60cm)

        logger.info("60cm直径柱子初始收缩完成")

    # 攀爬步骤函数
    def climb_one_step_upper(self):
        """上方杆攀爬一步"""
        logger.info("执行上方杆攀爬步骤...")

        # 1. 上方径向伸缩杆伸长5cm
        self.control_upper_radial_extend(self.extend_time)

        # 2. 上方舵机逆时针旋转5度
        self.rotate_upper_servo_ccw(5)

        # 3. 竖直伸缩杆伸长指定时间
        self.control_vertical_extend(self.vertical_extend_time)

        # 4. 上方舵机顺时针旋转回来5度
        self.rotate_upper_servo_cw(5)

        # 5. 上方径向伸缩杆收缩
        self.control_upper_radial_retract(self.extend_time)

        logger.info("上方杆攀爬步骤完成")

    def climb_one_step_lower(self):
        """下方杆攀爬一步"""
        logger.info("执行下方杆攀爬步骤...")

        # 1. 下方径向伸缩杆伸长5cm
        self.control_lower_radial_extend(self.extend_time)

        # 2. 下方舵机逆时针旋转5度
        self.rotate_lower_servo_ccw(5)

        # 3. 竖直伸缩杆伸长指定时间
        self.control_vertical_extend(self.vertical_extend_time)

        # 4. 下方舵机顺时针旋转回来5度
        self.rotate_lower_servo_cw(5)

        # 5. 下方径向伸缩杆收缩
        self.control_lower_radial_retract(self.extend_time)

        logger.info("下方杆攀爬步骤完成")

    def emergency_stop(self):
        """紧急停止"""
        logger.warning("紧急停止!")
        self.is_climbing = False

        # 立即停止所有径向伸缩杆输出
        GPIO.output(self.upper_radial_extend_pin, GPIO.LOW)
        GPIO.output(self.upper_radial_retract_pin, GPIO.LOW)
        GPIO.output(self.lower_radial_extend_pin, GPIO.LOW)
        GPIO.output(self.lower_radial_retract_pin, GPIO.LOW)

        # 立即停止所有水平伸缩杆输出
        GPIO.output(self.upper_horizontal_extend_pin, GPIO.LOW)
        GPIO.output(self.upper_horizontal_retract_pin, GPIO.LOW)
        GPIO.output(self.lower_horizontal_extend_pin, GPIO.LOW)
        GPIO.output(self.lower_horizontal_retract_pin, GPIO.LOW)

        # 立即停止竖直伸缩杆输出 - 确保两个继电器都断开
        GPIO.output(self.vertical_extend_pin, GPIO.LOW)
        GPIO.output(self.vertical_retract_pin, GPIO.LOW)

        # 重置舵机
        self.reset_servos()

        # 清理GPIO
        GPIO.cleanup()

        logger.info("紧急停止完成")

    def power_off(self):
        """关闭电源并清理资源"""
        logger.info("攀爬完成，关闭电源...")
        self.is_climbing = False

        # 重置舵机到中性位置
        self.reset_servos()

        # 停止PWM
        self.upper_servo.stop()
        self.lower_servo.stop()

        # 清理GPIO
        GPIO.cleanup()

        logger.info("系统已安全关闭")

    def __del__(self):
        """析构函数，确保GPIO被正确清理"""
        try:
            GPIO.cleanup()
        except:
            pass