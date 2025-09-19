#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单词发音文件生成脚本
"""

from gtts import gTTS
import os

# 按年级分类的缺失单词
missing_words = {
    "grade1": ["boy", "hand", "eye", "mouth", "red", "blue", "green", "one", "two", "three"],
    "grade2": ["bird", "pig", "head", "arm", "leg", "foot", "black", "white", "four", "five", "six", "classroom", "student"],
    "grade3": ["panda", "kangaroo", "finger", "toe", "hair", "purple", "pink", "seven", "eight", "nine", "ten", "playground", "library", "friend"]
}

def generate_pronunciations():
    """生成所有缺失的发音文件"""
    # 创建wordsounds目录结构
    os.makedirs("wordsounds", exist_ok=True)
    
    for grade, words in missing_words.items():
        print(f"正在生成 {grade} 单词发音...")
        
        for word in words:
            try:
                # 生成发音（英文）
                tts = gTTS(text=word, lang='en')
                filename = f"wordsounds/{word}.mp3"
                tts.save(filename)
                print(f"已生成: {filename}")
                
            except Exception as e:
                print(f"生成 {word} 发音失败: {str(e)}")

if __name__ == "__main__":
    print("开始生成单词发音文件...")
    generate_pronunciations()
    print("发音文件生成完成！")