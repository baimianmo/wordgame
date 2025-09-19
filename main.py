#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
背单词游戏主程序入口
适合一到三年级学生使用的图形界面单词学习游戏
包含学习模式、测试模式和拼写模式，拼写模式有简单、中等、复杂三种难度
"""

import tkinter as tk
import os
import sys
from game_ui import WordGameUI

def main():
    """主函数"""
    # 创建资源目录（如果不存在）
    if not os.path.exists("resources"):
        os.makedirs("resources")
    
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口样式
    root.configure(bg="#F0F8FF")
    
    # 创建游戏界面
    game_ui = WordGameUI(root)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()