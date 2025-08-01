#!/usr/bin/env python3
"""
测试robot.py中的上方径向杆控制功能
"""

from robot import ClimbingRobot
import time

def test_lower_radial():
    """测试上方径向杆功能"""
    print("开始测试robot.py中的上方径向杆功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("上方径向杆测试开始...")
        print("引脚配置:")
        print(f"- 伸长引脚: GPIO{robot.upper_radial_extend_pin}")
        print(f"- 收缩引脚: GPIO{robot.upper_radial_retract_pin}")
        print("按Ctrl+C退出\n")
        
        # 测试上方径向杆伸长
        # print("测试1: 上方径向杆伸长")
        # print(f"伸长时间: {robot.extend_time}秒")
        robot.control_upper_radial_extend(10)
        time.sleep(1)
        
        # 测试上方径向杆收缩
        # print("测试2: 上方径向杆收缩")
        # print(f"收缩时间: {robot.extend_time}秒")
        # robot.control_upper_radial_retract(robot.extend_time)
        # robot.control_upper_radial_retract(10)
        time.sleep(1)
        
        print("上方径向杆测试完成!")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_lower_radial()