#!/usr/bin/env python3
"""
测试final_extract函数
"""

from robot import ClimbingRobot
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_final_extract():
    """测试final_extract函数"""
    print("=== 测试final_extract函数 ===")
    
    try:
        # 创建机器人实例
        robot = ClimbingRobot()
        
        logger.info("机器人初始化完成")
        
        # 测试final_extract函数
        logger.info("开始测试final_extract函数...")
        robot.final_extend()
        
        logger.info("final_extract函数测试完成")
        
    except KeyboardInterrupt:
        logger.info("用户中断测试")
    
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
    
    finally:
        # 清理资源
        try:
            robot.reset_servos()
            time.sleep(1)
            robot.power_off()
            logger.info("机器人已安全关闭")
        except:
            pass

def main():
    """主函数"""
    print("final_extract函数测试程序")
    print("此程序将测试机器人的final_extract函数")
    print("该函数会同时伸长上下两个径向杆来松开对柱子的抓握")
    print("")
    
    # 开始测试
    test_final_extract()

if __name__ == "__main__":
    main()