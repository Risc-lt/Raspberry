#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
树莓派舵机控制程序
控制连接到GPIO 13的舵机转到90度位置
"""

import RPi.GPIO as GPIO
import time

# 设置GPIO引脚
SERVO_PIN = 12 # upper
# SERVO_PIN = 13 # lower

# 舵机角度对应的占空比
# 一般来说：0度=2.5%, 90度=7.5%, 180度=12.5%
ANGLE_0 = 2.5
ANGLE_90 = 7.5
ANGLE_180 = 12.5

def setup_servo():
    """初始化GPIO和PWM"""
    # 设置GPIO模式为BCM
    GPIO.setmode(GPIO.BCM)
    # 设置GPIO 13为输出模式
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    # 创建PWM实例，频率50Hz（舵机标准频率）
    pwm = GPIO.PWM(SERVO_PIN, 50)
    # 启动PWM，初始占空比为0
    pwm.start(0)
    return pwm

def set_servo_angle(pwm, angle):
    """设置舵机角度"""
    if angle == 0:
        duty_cycle = ANGLE_0
    elif angle == 90:
        duty_cycle = ANGLE_90
    elif angle == 180:
        duty_cycle = ANGLE_180
    else:
        # 线性插值计算其他角度的占空比
        duty_cycle = ANGLE_0 + (angle / 180.0) * (ANGLE_180 - ANGLE_0)
    
    # 设置占空比
    pwm.ChangeDutyCycle(duty_cycle)
    print(f"舵机转到 {angle} 度，占空比: {duty_cycle}%")

def cleanup():
    """清理GPIO资源"""
    GPIO.cleanup()
    print("GPIO资源已清理")

def main():
    """主函数"""
    try:
        print("初始化舵机控制...")
        pwm = setup_servo()
        
        print("舵机转到90度...")
        set_servo_angle(pwm, 90)
        
        print("舵机已转到90度位置并保持")
        print("按 Ctrl+C 退出程序")
        
        # 持续保持90度位置，直到用户按Ctrl+C退出
        while True:
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\n程序被用户中断，舵机停止")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 清理资源
        cleanup()

if __name__ == "__main__":
    main()