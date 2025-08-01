#!/usr/bin/env python3
"""
测试robot.py中的上方水平杆控制功能
"""

from robot import ClimbingRobot
import time

def test_lower_horizontal():
    """测试上方水平杆功能"""
    print("开始测试robot.py中的上方水平杆功能...")
    
    # 创建机器人对象
    robot = ClimbingRobot()
    
    try:
        print("上方水平杆测试开始...")
        print("引脚配置:")
        print(f"- 伸长引脚: GPIO{robot.upper_horizontal_extend_pin}")
        print(f"- 收缩引脚: GPIO{robot.upper_horizontal_retract_pin}")
        print("按Ctrl+C退出\n")
        
        # 测试上方水平杆收缩
        print("测试2: 上方水平杆收缩")
        print(f"收缩时间: 5秒")
        robot.control_upper_horizontal_retract(5)
        time.sleep(1)
        
        print("上方水平杆测试完成!")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    
    finally:
        # 清理资源
        robot.power_off()

if __name__ == "__main__":
    test_lower_horizontal()