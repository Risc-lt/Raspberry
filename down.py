#!/usr/bin/env python3
"""
下降攀爬控制 - 使用PID控制移动时间
"""

from robot import ClimbingRobot
from simple_pid import PID
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DownClimbController:
    def __init__(self, target_height=20):
        """
        初始化下降攀爬控制器
        :param target_height: 目标高度 (cm)
        """
        self.robot = ClimbingRobot()
        self.target_height = target_height
        
        # PID控制器参数（下降时参数可能需要调整）
        self.height_pid = PID(Kp=0.02, Ki=0.001, Kd=0.01, setpoint=target_height)
        self.height_pid.output_limits = (0.5, 3.0)  # 限制时间范围 0.5-3.0秒
        
        # 攀爬参数
        self.max_steps = 50  # 最大攀爬步数
        self.step_count = 0
        self.initial_height = 0
        self.height_threshold = 2.0  # 高度变化阈值 (cm)
        
        logger.info(f"下降攀爬控制器初始化完成，目标高度: {target_height}cm")

    def get_current_position(self):
        """获取当前位置（距离）"""
        return self.robot.get_current_height()

    def calculate_movement_time(self, current_height):
        """
        使用PID控制器计算移动时间
        :param current_height: 当前高度
        :return: 计算出的移动时间
        """
        # 计算高度差（当前 - 目标，下降时为正值）
        height_error = current_height - self.target_height
        
        # 使用PID控制器计算输出时间
        control_output = self.height_pid(current_height)
        
        logger.info(f"高度误差: {height_error:.2f}cm, PID输出时间: {control_output:.2f}秒")
        return control_output

    def climb_one_step_down(self, movement_time):
        """
        执行一步下降动作（反向攀爬）
        :param movement_time: PID计算出的移动时间
        """
        logger.info(f"=== 开始第 {self.step_count + 1} 步下降 ===")
        
        # 根据步数决定使用上方杆还是下方杆
        if self.step_count % 2 == 0:
            # 偶数步使用下方杆（下降时先用下方杆）
            logger.info("使用下方杆下降")
            
            # 1. 下方径向伸缩杆伸长
            self.robot.control_lower_radial_extend(movement_time)
            
            # 2. 下方舵机顺时针旋转（下降时方向相反）
            self.robot.rotate_lower_servo_cw(5)
            
            # 3. 竖直伸缩杆收缩（下降动作）
            self.robot.control_vertical_retract(movement_time)
            
            # 4. 下方舵机逆时针旋转回来
            self.robot.rotate_lower_servo_ccw(5)
            
            # 5. 下方径向伸缩杆收缩
            self.robot.control_lower_radial_retract(movement_time)
            
        else:
            # 奇数步使用上方杆
            logger.info("使用上方杆下降")
            
            # 1. 上方径向伸缩杆伸长
            self.robot.control_upper_radial_extend(movement_time)
            
            # 2. 上方舵机顺时针旋转（下降时方向相反）
            self.robot.rotate_upper_servo_cw(5)
            
            # 3. 竖直伸缩杆收缩（下降动作）
            self.robot.control_vertical_retract(movement_time)
            
            # 4. 上方舵机逆时针旋转回来
            self.robot.rotate_upper_servo_ccw(5)
            
            # 5. 上方径向伸缩杆收缩
            self.robot.control_upper_radial_retract(movement_time)
        
        self.step_count += 1
        logger.info(f"第 {self.step_count} 步下降完成")

    def check_progress(self, previous_height, current_height):
        """
        检查下降进度
        :param previous_height: 上一次测量的高度
        :param current_height: 当前测量的高度
        :return: True if making progress, False otherwise
        """
        height_change = abs(current_height - previous_height)
        
        if height_change < self.height_threshold:
            logger.warning(f"高度变化过小: {height_change:.2f}cm < {self.height_threshold}cm")
            return False
        
        # 检查是否在下降
        if current_height >= previous_height:
            logger.warning(f"未检测到下降，当前: {current_height:.2f}cm, 之前: {previous_height:.2f}cm")
            return False
        
        logger.info(f"下降距离: {height_change:.2f}cm")
        return True

    def start_climbing_down(self):
        """开始下降过程"""
        logger.info("=== 开始下降攀爬 ===")
        
        try:
            # 获取初始高度
            self.initial_height = self.get_current_position()
            logger.info(f"初始位置: {self.initial_height:.2f}cm")
            
            # 检查是否已经在目标高度附近
            if self.initial_height <= self.target_height + 5.0:
                logger.info("已经在目标高度附近，无需下降")
                return
            
            previous_height = self.initial_height
            
            while self.step_count < self.max_steps:
                # 获取当前高度
                current_height = self.get_current_position()
                logger.info(f"当前位置: {current_height:.2f}cm")
                
                # 检查下降进度（从第2步开始）
                if self.step_count > 0:
                    if not self.check_progress(previous_height, current_height):
                        logger.warning("下降进度不足，可能遇到障碍")
                        # 可以选择继续或停止
                
                # 使用PID控制器计算移动时间
                movement_time = self.calculate_movement_time(current_height)
                
                # 执行一步下降
                self.climb_one_step_down(movement_time)
                
                # 检查是否达到目标高度
                current_height = self.get_current_position()
                height_to_target = current_height - self.target_height
                if height_to_target <= 2.0:  # 2cm容忍度
                    logger.info(f"已达到目标高度! 当前: {current_height:.2f}cm, 目标: {self.target_height}cm")
                    # 如果是偶数步完成，需要继续执行下一步（奇数步）来回收竖直杆
                    if self.step_count % 2 == 0:
                        logger.info("偶数步完成，继续执行下一步回收竖直杆...")
                        # 使用固定时间来执行下一步，而不是PID计算的时间
                        self.climb_one_step_down(3.0)  # TODO:
                    break
                
                # 等待稳定
                time.sleep(1)
                
                # 更新上一次高度
                previous_height = current_height
                
                # 显示进度
                total_progress = self.initial_height - current_height
                logger.info(f"总下降: {total_progress:.2f}cm, 剩余: {height_to_target:.2f}cm")
            
            # 下降结束
            final_height = self.get_current_position()
            total_descent = self.initial_height - final_height
            
            logger.info("=== 下降完成 ===")
            logger.info(f"初始高度: {self.initial_height:.2f}cm")
            logger.info(f"最终高度: {final_height:.2f}cm")
            logger.info(f"总下降距离: {total_descent:.2f}cm")
            logger.info(f"总步数: {self.step_count}")
            
        except KeyboardInterrupt:
            logger.info("用户中断下降")
        
        except Exception as e:
            logger.error(f"下降过程中出错: {e}")
        
        finally:
            # 重置舵机并清理
            self.robot.reset_servos()
            time.sleep(1)
            self.robot.final_extract()
            self.robot.power_off()

def main():
    """主函数"""
    print("下降攀爬控制程序")
    target = 0.0 # TODO:
    
    # 创建下降控制器
    controller = DownClimbController(target_height=target)
    
    # 开始下降
    controller.start_climbing_down()

if __name__ == "__main__":
    main()