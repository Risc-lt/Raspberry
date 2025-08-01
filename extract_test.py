#!/usr/bin/env python3
"""
测试初始收缩函数 - 30cm和60cm直径柱子
"""

from robot import ClimbingRobot
import time
import logging
import argparse

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_initial_retraction_30cm():
    """测试30cm直径柱子的初始收缩函数"""
    print("=== 测试30cm直径柱子初始收缩函数 ===")
    
    try:
        # 创建机器人实例
        robot = ClimbingRobot()
        
        logger.info("机器人初始化完成")
        
        # 测试30cm初始收缩函数
        logger.info("开始测试30cm直径柱子初始收缩函数...")
        robot.initial_retraction_30cm()
        
        logger.info("30cm初始收缩函数测试完成")
        
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

def test_initial_retraction_60cm():
    """测试60cm直径柱子的初始收缩函数"""
    print("=== 测试60cm直径柱子初始收缩函数 ===")
    
    try:
        # 创建机器人实例
        robot = ClimbingRobot()
        
        logger.info("机器人初始化完成")
        
        # 测试60cm初始收缩函数
        logger.info("开始测试60cm直径柱子初始收缩函数...")
        robot.initial_retraction_60cm()
        
        logger.info("60cm初始收缩函数测试完成")
        
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
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='初始收缩函数测试程序')
    parser.add_argument('-r', '--radius', type=int, choices=[30, 60], 
                       help='柱子直径 (30 或 60)')
    
    args = parser.parse_args()
    
    print("初始收缩函数测试程序")
    print("此程序将测试机器人的初始收缩函数")
    print("测试径向杆和水平杆的收缩功能，使机器人能够抓紧不同直径的柱子")
    print("")
    
    if args.radius == 30:
        # 测试30cm
        test_initial_retraction_30cm()
    elif args.radius == 60:
        # 测试60cm
        test_initial_retraction_60cm()
    else:
        # 没有参数，询问用户选择
        print("请选择测试模式:")
        print("1. 测试30cm直径柱子初始收缩")
        print("2. 测试60cm直径柱子初始收缩")
        
        try:
            choice = input("请输入选择 (1/2): ")
            
            if choice == '1':
                test_initial_retraction_30cm()
            elif choice == '2':
                test_initial_retraction_60cm()
            else:
                print("无效选择")
                
        except KeyboardInterrupt:
            print("\n用户取消测试")

if __name__ == "__main__":
    main()