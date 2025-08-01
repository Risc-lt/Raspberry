#!/usr/bin/env python3
"""
测试robot.py中的下方水平杆控制功能
"""

from robot import ClimbingRobot
import time

def test_lower_horizontal():
    """测试下方水平杆功能"""
    print("开始测试robot.py中的下方水平杆功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("下方水平杆测试开始...")
        print("引脚配置:")
        print(f"- 伸长引脚: GPIO{robot.lower_horizontal_extend_pin}")
        print(f"- 收缩引脚: GPIO{robot.lower_horizontal_retract_pin}")
        print("按Ctrl+C退出\n")
        
        # 测试下方水平杆伸长
        print("测试1: 下方水平杆伸长")
        print(f"伸长时间: {robot.extend_time}秒")
        robot.control_lower_horizontal_extend(robot.extend_time)
        time.sleep(1)
        
        # 测试下方水平杆收缩
        print("测试2: 下方水平杆收缩")
        print(f"收缩时间: {robot.extend_time}秒")
        robot.control_lower_horizontal_retract(robot.extend_time)
        time.sleep(1)
        
        print("下方水平杆测试完成!")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_lower_horizontal()