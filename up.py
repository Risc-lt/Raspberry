#!/usr/bin/env python3
"""
上升攀爬控制 - 手动定义步数和移动时间
"""

from robot import ClimbingRobot
import time
import logging
import argparse

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UpClimbController:
    def __init__(self, total_steps=10, movement_time=2.0):
        """
        初始化上升攀爬控制器
        :param total_steps: 总攀爬步数
        :param movement_time: 每次移动时间 (秒)
        """
        self.robot = ClimbingRobot()
        self.total_steps = total_steps
        self.movement_time = movement_time
        
        # 攀爬参数
        self.step_count = 0
        self.initial_height = 0
        self.height_threshold = 2.0  # 高度变化阈值 (cm)
        
        logger.info(f"上升攀爬控制器初始化完成，总步数: {total_steps}，每次移动时间: {movement_time}秒")

    def get_current_position(self):
        """获取当前位置（距离）"""
        return self.robot.get_current_height()

    def climb_one_step(self):
        """
        执行一步攀爬动作
        """
        logger.info(f"=== 开始第 {self.step_count + 1} 步攀爬 ===")
        
        # 根据步数决定使用上方杆还是下方杆
        if self.step_count % 2 == 0:
            # 偶数步使用上方杆
            logger.info("使用上方杆攀爬")
            
            # 1. 上方径向伸缩杆伸长
            self.robot.control_upper_radial_extend(self.movement_time)
            
            # 2. 上方舵机逆时针旋转
            # self.robot.rotate_upper_servo_ccw(5)
            
            # 3. 竖直伸缩杆伸长
            self.robot.control_vertical_extend(self.movement_time)
            
            # 4. 上方舵机顺时针旋转回来
            # self.robot.rotate_upper_servo_cw(5)
            
            # 5. 上方径向伸缩杆收缩
            self.robot.control_upper_radial_retract(self.movement_time)
            
        else:
            # 奇数步使用下方杆
            logger.info("使用下方杆攀爬")
            
            # 1. 下方径向伸缩杆伸长
            self.robot.control_lower_radial_extend(self.movement_time)
            
            # 2. 下方舵机逆时针旋转
            # self.robot.rotate_lower_servo_ccw(5)
            
            # 3. 竖直伸缩杆伸长
            self.robot.control_vertical_extend(self.movement_time)
            
            # 4. 下方舵机顺时针旋转回来
            # self.robot.rotate_lower_servo_cw(5)
            
            # 5. 下方径向伸缩杆收缩
            self.robot.control_lower_radial_retract(self.movement_time)
        
        self.step_count += 1
        logger.info(f"第 {self.step_count} 步攀爬完成")

    def check_progress(self, previous_height, current_height):
        """
        检查攀爬进度
        :param previous_height: 上一次测量的高度
        :param current_height: 当前测量的高度
        :return: True if making progress, False otherwise
        """
        height_change = abs(current_height - previous_height)
        
        if height_change < self.height_threshold:
            logger.warning(f"高度变化过小: {height_change:.2f}cm < {self.height_threshold}cm")
            return False
        
        logger.info(f"高度变化: {height_change:.2f}cm")
        return True

    def start_climbing(self):
        """开始攀爬过程"""
        logger.info("=== 开始上升攀爬 ===")
        
        try:
            # 获取初始高度
            self.initial_height = self.get_current_position()
            logger.info(f"初始位置: {self.initial_height:.2f}cm")
            
            previous_height = self.initial_height
            
            while self.step_count < self.total_steps:
                # 获取当前高度
                current_height = self.get_current_position()
                logger.info(f"当前位置: {current_height:.2f}cm")
                
                # 检查攀爬进度（从第2步开始）
                if self.step_count > 0:
                    if not self.check_progress(previous_height, current_height):
                        logger.warning("攀爬进度不足，可能遇到障碍")
                        # 可以选择继续或停止
                
                # 执行一步攀爬
                self.climb_one_step()
                
                # 等待稳定
                time.sleep(1)
                
                # 更新上一次高度
                previous_height = current_height
                
                # 显示进度
                current_height = self.get_current_position()
                total_progress = current_height - self.initial_height
                logger.info(f"总进度: {total_progress:.2f}cm, 已完成步数: {self.step_count}/{self.total_steps}")
            
            # 攀爬结束
            final_height = self.get_current_position()
            total_climb = final_height - self.initial_height
            
            logger.info("=== 攀爬完成 ===")
            logger.info(f"初始高度: {self.initial_height:.2f}cm")
            logger.info(f"最终高度: {final_height:.2f}cm")
            logger.info(f"总攀爬距离: {total_climb:.2f}cm")
            logger.info(f"总步数: {self.step_count}")
            
        except KeyboardInterrupt:
            logger.info("用户中断攀爬")
        
        except Exception as e:
            logger.error(f"攀爬过程中出错: {e}")
        
        finally:
            # 重置舵机并清理
            self.robot.reset_servos()
            time.sleep(1)
            self.robot.power_off()

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='上升攀爬控制程序')
    parser.add_argument('-r', '--radius', type=int, choices=[30, 60], 
                       help='柱子直径 (30 或 60)')
    
    args = parser.parse_args()
    
    print("上升攀爬控制程序")
    
    # 检查是否提供了 -r 参数
    if args.radius:
        logger.info(f"检测到 -r 参数，柱子直径: {args.radius}cm")
        
        # 创建机器人实例执行初始收缩
        robot = ClimbingRobot()
        
        try:
            if args.radius == 30:
                logger.info("执行30cm直径柱子初始收缩")
                robot.initial_retraction_30cm()
            elif args.radius == 60:
                logger.info("执行60cm直径柱子初始收缩")
                robot.initial_retraction_60cm()
            
            logger.info("初始收缩完成，程序结束")
            
        except Exception as e:
            logger.error(f"初始收缩过程中出错: {e}")
        
        finally:
            robot.power_off()
    
    else:
        # 没有 -r 参数，执行正常攀爬
        total_steps = 2  # 手动定义总步数
        movement_time = 10.0  # 手动定义每次移动时间(秒)
        
        # 创建攀爬控制器
        controller = UpClimbController(total_steps=total_steps, movement_time=movement_time)
        
        # 开始攀爬
        controller.start_climbing()

if __name__ == "__main__":
    main()