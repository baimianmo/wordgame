#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单词游戏图形界面模块
"""

import tkinter as tk
from tkinter import messagebox
import os
import warnings

# 处理pygame导入
pygame_available = False
try:
    import pygame
    pygame.mixer.init()
    pygame_available = True
except ImportError:
    pass

from game_logic import WordGame

class WordGameUI:
    def __init__(self, master):
        self.master = master
        self.game = WordGame()
        self.auto_pronounce = True  # 控制自动发音
        
        # 创建主框架
        self.create_main_frames()
        
        # 创建控制区域
        self.create_control_area()
        
        # 创建单词显示区域
        self.create_word_area()
        
        # 创建拼写模式组件
        self.create_spelling_components()
        
        # 创建底部控制按钮
        self.create_bottom_controls()
        
        # 默认设置一年级
        self.game.set_grade("一年级")
        self.layout_ui()
        self.switch_mode("学习模式")
    
    def create_main_frames(self):
        """创建主框架"""
        self.left_frame = tk.Frame(self.master, width=150, bg="#f0f0f0")
        self.main_frame = tk.Frame(self.master)
        self.right_frame = None
        
    def create_control_area(self):
        """创建控制区域"""
        self.control_frame = tk.Frame(self.main_frame)
        self.mode_frame = tk.Frame(self.control_frame)
        
        self.learn_btn = tk.Button(self.mode_frame, text="学习模式", 
                                 command=lambda: self.switch_mode("学习模式"))
        self.test_btn = tk.Button(self.mode_frame, text="测试模式", 
                                command=lambda: self.switch_mode("测试模式"))
        self.spell_btn = tk.Button(self.mode_frame, text="拼写模式", 
                                 command=lambda: self.switch_mode("拼写模式"))
        
    def create_word_area(self):
        """创建单词显示区域"""
        self.word_frame = tk.Frame(self.main_frame)
        self.word_label = tk.Label(self.word_frame, font=("Arial", 32))
        self.translation_label = tk.Label(self.word_frame, font=("Arial", 20))
        self.result_label = tk.Label(self.word_frame, font=("Arial", 16))
        
        # 测试模式组件
        self.test_answer_entry = tk.Entry(self.word_frame, font=("Arial", 16))
        
    def create_spelling_components(self):
        """创建拼写模式组件"""
        # 确保主框架存在
        if not hasattr(self, 'main_frame'):
            self.main_frame = tk.Frame(self.master)
            self.main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
            
        # 创建拼写框架
        self.spelling_frame = tk.Frame(self.main_frame)
        self.spelling_frame.pack(pady=20)
        
        # 创建输入框和控制按钮框架
        self.input_frame = tk.Frame(self.spelling_frame)
        self.input_frame.pack(pady=10)
        
        # 输入框
        self.spelling_entry = tk.Entry(self.input_frame, 
                                    font=("Arial", 24), 
                                    width=20)
        self.spelling_entry.pack(side=tk.LEFT, padx=5)
        
        # 提交按钮
        self.submit_btn = tk.Button(self.input_frame, text="提交", width=5, font=("Arial", 12),
                                  command=self.check_spelling)
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        # 创建键盘框架
        self.keyboard_frame = tk.Frame(self.spelling_frame)
        self.keyboard_frame.pack(pady=10)
        
        # 创建键盘按钮
        self.create_keyboard_buttons()
        
        # 默认隐藏
        self.spelling_frame.pack_forget()
        
    def create_keyboard_buttons(self):
        """创建键盘按钮"""
        # 创建键盘行框架并立即布局
        row1 = tk.Frame(self.keyboard_frame)
        row1.pack()
        row2 = tk.Frame(self.keyboard_frame)
        row2.pack()
        row3 = tk.Frame(self.keyboard_frame)
        row3.pack()
        
        # 第一行字母 QWERTYUIOP
        for char in "QWERTYUIOP":
            btn = tk.Button(row1, text=char, width=3, font=("Arial", 14),
                         command=lambda c=char: self.append_letter(c.lower()))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # 第二行字母 ASDFGHJKL
        for char in "ASDFGHJKL":
            btn = tk.Button(row2, text=char, width=3, font=("Arial", 14),
                         command=lambda c=char: self.append_letter(c.lower()))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # 第三行字母 ZXCVBNM
        for char in "ZXCVBNM":
            btn = tk.Button(row3, text=char, width=3, font=("Arial", 14),
                         command=lambda c=char: self.append_letter(c.lower()))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 确保键盘框架可见
        self.keyboard_frame.pack(pady=10)
        
    def create_bottom_controls(self):
        """创建底部控制按钮"""
        self.bottom_frame = tk.Frame(self.main_frame)
        self.next_btn = tk.Button(self.bottom_frame, text="下一个", 
                                command=self.next_word)
        self.pronounce_btn = tk.Button(self.bottom_frame, text="发音", 
                                     command=self.play_pronunciation)
        
    def layout_ui(self):
        """布局UI组件"""
        self.master.title(f"小学生单词游戏 - {self.game.current_grade}")
        self.master.geometry("1000x600")
        
        # 布局左侧年级选择区域
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_frame.pack_propagate(False)
        
        # 创建年级选择框区
        self.grade_frame = tk.Frame(self.left_frame, bg="#f0f0f0", bd=1, relief=tk.SOLID)
        self.grade_frame.pack(pady=(5,20), padx=5, fill=tk.X)
        
        # 创建难度选择框区（初始隐藏）
        self.difficulty_frame = tk.Frame(self.left_frame, bg="#f0f0f0", bd=1, relief=tk.SOLID)
        tk.Label(self.difficulty_frame, text="选择难度", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        
        for difficulty in ["简单", "中等", "困难"]:
            btn = tk.Button(
                self.difficulty_frame,
                text=difficulty,
                width=10,
                command=lambda d=difficulty: self.set_difficulty_and_start(d),
                relief=tk.RAISED if difficulty == "简单" else tk.FLAT
            )
            btn.pack(pady=5)
        
        # 添加年级选择标题
        tk.Label(self.grade_frame, 
                text="年级选择", 
                font=("Arial", 14), 
                bg="#f0f0f0").pack(pady=(5,10))
        
        # 创建年级选择按钮
        self.grade_buttons = {}
        for grade in ["一年级", "二年级", "三年级"]:
            btn = tk.Button(
                self.grade_frame,
                text=grade,
                width=10,
                command=lambda g=grade: self.change_grade(g),
                bg="#e0e0e0" if grade != self.game.current_grade else "#a0c0ff"
            )
            btn.pack(pady=2)
            self.grade_buttons[grade] = btn
            
        # 布局右侧主内容区域
        self.main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # 布局控制区域
        self.control_frame.pack(pady=10)
        self.mode_frame.pack()
        self.learn_btn.pack(side=tk.LEFT, padx=5)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        self.spell_btn.pack(side=tk.LEFT, padx=5)
        
        # 布局单词显示区域（合并中英文）
        self.word_frame.pack(pady=20)
        self.word_label.config(font=("Arial", 28))
        self.word_label.pack()
        # 不再单独显示翻译标签
        self.translation_label.pack_forget() 
        self.result_label.pack(pady=5)
        
        # 布局底部控制按钮
        self.bottom_frame.pack(pady=20)
        self.next_btn.pack(side=tk.LEFT, padx=10)
        self.pronounce_btn.pack(side=tk.LEFT, padx=10)
        
    def clear_window(self):
        """清除窗口所有组件"""
        if hasattr(self, 'master') and self.master:
            for widget in self.master.winfo_children():
                widget.destroy()
        
        # 重新创建所有组件
        self.create_main_frames()
        self.create_control_area()
        self.create_word_area()
        self.create_spelling_components()
        self.create_bottom_controls()
        self.layout_ui()
        
    def change_grade(self, grade):
        """切换年级"""
        self.game.set_grade(grade)
        # 更新按钮背景色
        for g, btn in self.grade_buttons.items():
            btn.config(bg="#a0c0ff" if g == grade else "#e0e0e0")
        # 刷新当前模式
        self.switch_mode(self.game.game_mode)
        
    def append_letter(self, letter):
        """添加字母"""
        self.spelling_entry.insert(tk.END, letter)
        
    def delete_letter(self):
        """删除字母"""
        current = self.spelling_entry.get()
        if current:
            self.spelling_entry.delete(len(current)-1, tk.END)
            
    def check_test_answer(self):
        """检查测试答案"""
        user_input = self.test_answer_entry.get()
        correct = self.game.check_test_answer(user_input)
        
        if correct:
            self.result_label.config(text="✓ 回答正确", fg="green")
        else:
            self.result_label.config(
                text=f"✗ 回答错误，正确答案: {self.game.current_word['translation']}", 
                fg="red"
            )
        self.master.after(3000, self.next_word)
            
    def check_spelling(self):
        """检查拼写"""
        user_input = self.spelling_entry.get().lower()
        correct = self.game.check_spelling(user_input)
        
        if correct:
            # 显示完整单词
            self.word_label.config(text=self.game.current_word["word"])
            self.result_label.config(text="✓ 拼写正确", fg="green")
            self.spelling_entry.delete(0, tk.END)
            # 1秒后切换到下一个单词
            self.master.after(1000, self.next_word)
        else:
            self.result_label.config(
                text=f"✗ 拼写错误，正确答案: {self.game.current_word['word']}", 
                fg="red"
            )
            self.spelling_entry.delete(0, tk.END)
            self.spelling_entry.focus()
            self.master.after(3000, self.clear_feedback)
            
    def fade_out_feedback(self):
        """淡出反馈"""
        current_text = self.result_label.cget("text")
        if current_text:
            new_text = current_text[:-1] if len(current_text) > 1 else ""
            self.result_label.config(text=new_text)
            if new_text:
                self.master.after(100, self.fade_out_feedback)
            else:
                self.clear_feedback()
                
    def clear_feedback(self):
        """清除反馈"""
        self.result_label.config(text="")
            
    def next_word(self):
        """下一个单词"""
        self.switch_mode(self.game.game_mode)
        
        # 自动播放当前单词发音
        if pygame_available and self.auto_pronounce:
            self.master.after(500, self.play_pronunciation)  # 延迟确保UI更新完成
        
    def play_pronunciation(self):
        """播放发音"""
        if not pygame_available:
            messagebox.showwarning("提示", "发音功能不可用，请安装pygame库")
            return
            
        if self.game.current_word:
            word = self.game.current_word["word"]
            sound_file = f"wordsounds/{word}.mp3"
            if os.path.exists(sound_file):
                try:
                    # 初始化混音器（避免重复初始化）
                    if not pygame.mixer.get_init():
                        pygame.mixer.init(frequency=44100, size=-16, channels=2)
                    
                    # 使用Sound对象替代music模块（更稳定）
                    sound = pygame.mixer.Sound(sound_file)
                    sound.play()
                except Exception as e:
                    print(f"发音播放错误: {str(e)}")
                    # 尝试重新生成问题文件
                    self.regenerate_pronunciation(word)
            else:
                messagebox.showwarning("提示", f"发音文件不存在: {sound_file}")

    def regenerate_pronunciation(self, word):
        """重新生成问题发音文件"""
        try:
            from gtts import gTTS
            tts = gTTS(text=word, lang='en')
            tts.save(f"wordsounds/{word}.mp3")
            print(f"已重新生成: wordsounds/{word}.mp3")
        except Exception as e:
            print(f"重新生成发音文件失败: {str(e)}")

    def switch_mode(self, mode):
        """切换模式"""
        self.game.game_mode = mode
        self.clear_feedback()
        
        # 首次切换模式时自动发音
        if pygame_available and self.auto_pronounce:
            self.master.after(500, self.play_pronunciation)
        
        # 隐藏所有模式特定的组件
        self.spelling_frame.pack_forget()
        self.test_answer_entry.pack_forget()
        if hasattr(self, 'keyboard_frame') and self.keyboard_frame:
            self.keyboard_frame.pack_forget()
        
        # 清除右侧难度选择区域
        if hasattr(self, 'right_frame') and self.right_frame is not None:
            self.right_frame.destroy()
            self.right_frame = None
        
        if mode == "学习模式":
            # 隐藏难度选择框
            if hasattr(self, 'difficulty_frame'):
                self.difficulty_frame.pack_forget()
            word = self.game.generate_learning_word()
            self.word_label.config(text=f"{word['word']} - {word['translation']}")
            self.translation_label.config(text="")
            
        elif mode == "测试模式":
            # 隐藏难度选择框
            if hasattr(self, 'difficulty_frame'):
                self.difficulty_frame.pack_forget()
            word = self.game.generate_test_word()
            self.word_label.config(text=word["word"])
            self.translation_label.config(text="")
            self.test_answer_entry.pack(pady=10)
            self.test_answer_entry.focus()
            self.test_answer_entry.bind("<Return>", lambda e: self.check_test_answer())
            
        elif mode == "拼写模式":
            # 显示难度选择框区
            self.difficulty_frame.pack(pady=(0,5), padx=5, fill=tk.X)
            
            # 默认选择简单难度
            self.game.set_spelling_difficulty("简单")
            
            # 开始拼写模式
            self.set_difficulty_and_start("简单")

    def set_difficulty_and_start(self, difficulty):
        """设置难度并开始"""
        # 确保右侧框架存在
        if not hasattr(self, 'right_frame') or not self.right_frame:
            return
            
        # 更新按钮样式
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(relief=tk.RAISED if widget["text"] == difficulty else tk.FLAT)
        
        self.game.set_spelling_difficulty(difficulty)
        
        # 生成单词
        word = self.game.generate_spelling_word()
        self.word_label.config(text=f"{word['hint']} - {word['translation']}")
        self.translation_label.config(text="")
        
        # 确保拼写组件存在
        if not hasattr(self, 'spelling_frame'):
            self.create_spelling_components()
            
        # 显示所有拼写组件
        self.spelling_frame.pack(pady=20)
        self.spelling_entry.pack(pady=10)
        self.keyboard_frame.pack(pady=10)
        
        # 重置输入框状态
        self.spelling_entry.delete(0, tk.END)
        self.spelling_entry.focus()
        self.spelling_entry.bind("<Return>", lambda e: self.check_spelling())
        
        # 强制刷新UI
        self.master.update_idletasks()
        self.master.update()
                
    def set_difficulty_and_start(self, difficulty):
        """设置难度并开始"""
        # 更新按钮样式
        for widget in self.difficulty_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(relief=tk.RAISED if widget["text"] == difficulty else tk.FLAT)
        
        self.game.set_spelling_difficulty(difficulty)
        
        word = self.game.generate_spelling_word()
        self.word_label.config(text=f"{word['hint']} - {word['translation']}")
        self.translation_label.config(text="")
        self.spelling_frame.pack(pady=5)
        self.keyboard_frame.pack()
        self.spelling_entry.delete(0, tk.END)
        self.spelling_entry.focus()
        self.spelling_entry.bind("<Return>", lambda e: self.check_spelling())

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameUI(root)
    root.mainloop()