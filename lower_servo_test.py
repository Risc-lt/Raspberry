#!/usr/bin/env python3
"""
测试robot.py中的舵机控制功能
"""

from robot import ClimbingRobot
import time

def test_servo():
    """测试舵机功能"""
    print("开始测试robot.py中的舵机功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("舵机测试开始...")
        print("下方舵机(GPIO13)将执行旋转测试")
        print("按Ctrl+C退出\n")
        
        # 测试下方舵机逆时针旋转5度（杆向后）
        print("测试1: 下方舵机逆时针旋转5度（杆向后）")
        robot.rotate_lower_servo_ccw(5)
        time.sleep(2)
        
        # 测试下方舵机顺时针旋转5度（杆向前）
        print("测试2: 下方舵机顺时针旋转5度（杆向前）")
        robot.rotate_lower_servo_cw(5)
        time.sleep(2)
        
        # 重置到中性位置
        print("测试3: 重置舵机到中性位置")
        robot.reset_servos()
        time.sleep(2)
        
        print("舵机测试完成!")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_servo()