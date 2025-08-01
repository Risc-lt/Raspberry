#!/usr/bin/env python3
"""
测试robot.py中的竖直杆控制功能
"""

from robot import ClimbingRobot
import time

def test_vertical():
    """测试竖直杆功能"""
    print("开始测试robot.py中的竖直杆功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("竖直杆测试开始...")
        print("引脚配置:")
        print(f"- 伸长引脚: GPIO{robot.vertical_extend_pin}")
        print(f"- 收缩引脚: GPIO{robot.vertical_retract_pin}")
        print("按Ctrl+C退出\n")
        
        # 测试竖直杆伸长
        # print("测试1: 竖直杆伸长")
        # print(f"伸长时间: {robot.vertical_extend_time}秒")
        # robot.control_vertical_extend(15)
        # time.sleep(1)
        
        # 测试竖直杆收缩
        # print("测试2: 竖直杆收缩")
        # print(f"收缩时间: {robot.vertical_extend_time}秒")
        robot.control_vertical_retract(15)
        # time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n测试中断")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_vertical()