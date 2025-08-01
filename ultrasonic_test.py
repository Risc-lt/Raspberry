#!/usr/bin/env python3
"""
测试robot.py中的超声波测距功能
"""

from robot import ClimbingRobot
import time

def test_ultrasonic():
    """测试超声波传感器功能"""
    print("开始测试robot.py中的超声波功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("超声波测试开始...")
        print("按Ctrl+C退出\n")
        
        while True:
            # 调用robot类中的超声波测量函数
            distance = robot.get_current_height()
            
            if distance > 0:
                print(f"检测距离: {distance} cm")
            else:
                print("测量失败或超出范围")
            
            time.sleep(0.5)  # 每0.5秒测量一次
            
    except KeyboardInterrupt:
        print("\n测试结束")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_ultrasonic()