#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单词游戏逻辑模块
"""

import random

class WordGame:
    def __init__(self):
        self.current_grade = "一年级"
        self.game_mode = "学习模式"
        self.current_word = None
        self.current_words = []
        self.spelling_difficulty = "简单"
        self.used_words = []  # 记录已用单词
        self.load_words()
        
    def load_words(self):
        """加载单词数据"""
        # 模拟单词数据 - 实际项目中应从文件或数据库加载
        grade_words = {
            "一年级": [
                {"word": "apple", "translation": "苹果"},
                {"word": "book", "translation": "书"},
                {"word": "cat", "translation": "猫"},
                {"word": "dog", "translation": "狗"},
                {"word": "egg", "translation": "鸡蛋"},
                {"word": "fish", "translation": "鱼"},
                {"word": "girl", "translation": "女孩"},
                {"word": "boy", "translation": "男孩"},
                {"word": "hand", "translation": "手"},
                {"word": "eye", "translation": "眼睛"},
                {"word": "nose", "translation": "鼻子"},
                {"word": "mouth", "translation": "嘴巴"},
                {"word": "red", "translation": "红色"},
                {"word": "blue", "translation": "蓝色"},
                {"word": "green", "translation": "绿色"},
                {"word": "one", "translation": "一"},
                {"word": "two", "translation": "二"},
                {"word": "three", "translation": "三"},
                {"word": "school", "translation": "学校"},
                {"word": "teacher", "translation": "老师"}
            ],
            "二年级": [
                {"word": "dog", "translation": "狗"},
                {"word": "egg", "translation": "鸡蛋"},
                {"word": "fish", "translation": "鱼"},
                {"word": "bird", "translation": "鸟"},
                {"word": "rabbit", "translation": "兔子"},
                {"word": "pig", "translation": "猪"},
                {"word": "monkey", "translation": "猴子"},
                {"word": "tiger", "translation": "老虎"},
                {"word": "head", "translation": "头"},
                {"word": "arm", "translation": "手臂"},
                {"word": "leg", "translation": "腿"},
                {"word": "foot", "translation": "脚"},
                {"word": "yellow", "translation": "黄色"},
                {"word": "black", "translation": "黑色"},
                {"word": "white", "translation": "白色"},
                {"word": "four", "translation": "四"},
                {"word": "five", "translation": "五"},
                {"word": "six", "translation": "六"},
                {"word": "classroom", "translation": "教室"},
                {"word": "student", "translation": "学生"}
            ],
            "三年级": [
                {"word": "girl", "translation": "女孩"},
                {"word": "house", "translation": "房子"},
                {"word": "ice", "translation": "冰"},
                {"word": "elephant", "translation": "大象"},
                {"word": "panda", "translation": "熊猫"},
                {"word": "lion", "translation": "狮子"},
                {"word": "kangaroo", "translation": "袋鼠"},
                {"word": "finger", "translation": "手指"},
                {"word": "toe", "translation": "脚趾"},
                {"word": "hair", "translation": "头发"},
                {"word": "orange", "translation": "橙色"},
                {"word": "purple", "translation": "紫色"},
                {"word": "pink", "translation": "粉色"},
                {"word": "seven", "translation": "七"},
                {"word": "eight", "translation": "八"},
                {"word": "nine", "translation": "九"},
                {"word": "ten", "translation": "十"},
                {"word": "playground", "translation": "操场"},
                {"word": "library", "translation": "图书馆"},
                {"word": "friend", "translation": "朋友"}
            ]
        }
        self.current_words = grade_words.get(self.current_grade, [])
        return self.current_words
        
    def set_grade(self, grade):
        """设置年级"""
        self.current_grade = grade
        self.load_words()
        
    def set_game_mode(self, mode):
        """设置游戏模式"""
        self.game_mode = mode
        
    def set_spelling_difficulty(self, difficulty):
        """设置拼写难度"""
        self.spelling_difficulty = difficulty
        
    def generate_learning_word(self):
        """生成学习单词"""
        if not self.current_words:
            self.load_words()
            
        # 过滤掉已用单词
        available_words = [w for w in self.current_words 
                          if w["word"] not in self.used_words]
        
        # 如果所有单词都用过，重置记录
        if not available_words:
            self.used_words = []
            available_words = self.current_words
            
        self.current_word = random.choice(available_words)
        self.used_words.append(self.current_word["word"])
        return {
            "word": self.current_word["word"],
            "translation": self.current_word["translation"]
        }
        
    def generate_test_word(self):
        """生成测试单词"""
        if not self.current_words:
            self.load_words()
            
        # 过滤掉已用单词
        available_words = [w for w in self.current_words 
                         if w["word"] not in self.used_words]
        
        # 如果所有单词都用过，重置记录
        if not available_words:
            self.used_words = []
            available_words = self.current_words
            
        self.current_word = random.choice(available_words)
        self.used_words.append(self.current_word["word"])
        return {
            "word": self.current_word["word"],
            "translation": "",  # 测试模式不显示翻译
            "correct_answer": self.current_word["translation"]  # 保存正确答案
        }
        
    def generate_spelling_word(self):
        """生成拼写单词"""
        if not self.current_words:
            self.load_words()
            
        # 过滤掉已用单词
        available_words = [w for w in self.current_words 
                         if w["word"] not in self.used_words]
        
        # 如果所有单词都用过，重置记录
        if not available_words:
            self.used_words = []
            available_words = self.current_words
            
        self.current_word = random.choice(available_words)
        self.used_words.append(self.current_word["word"])
        
        hint = ""
        word = self.current_word["word"]
        
        if self.spelling_difficulty == "简单":
            # 显示首字母和部分字母
            hint = word[0] + "_" * (len(word)-1)
        elif self.spelling_difficulty == "中等":
            # 显示首尾字母
            hint = word[0] + "_" * (len(word)-2) + word[-1] if len(word) > 1 else word
        else:
            # 困难模式 - 全部隐藏
            hint = "_" * len(word)
            
        return {
            "word": word,
            "hint": hint,
            "translation": self.current_word["translation"]
        }
        
    def check_spelling(self, user_input):
        """检查拼写"""
        if not hasattr(self, 'current_word') or not self.current_word:
            return False
        return user_input.lower() == self.current_word["word"].lower()
        
    def check_test_answer(self, user_answer):
        """检查测试答案"""
        if not hasattr(self, 'current_word') or not self.current_word:
            return False
        return user_answer.strip().lower() == self.current_word["translation"].lower()