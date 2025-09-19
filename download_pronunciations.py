import os
import requests
from bs4 import BeautifulSoup
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# 导入单词数据
try:
    from words_data import GRADE_1_WORDS as grade1_words
    from words_data import GRADE_2_WORDS as grade2_words
    from words_data import GRADE_3_WORDS as grade3_words
except ImportError:
    print("错误: 找不到words_data.py文件或格式不正确")
    exit(1)

# 全局变量
DOWNLOADED_FILE = "downloaded_words.txt"
MAX_WORKERS = 5  # 最大线程数
RETRY_TIMES = 3   # 重试次数

def load_downloaded_words():
    """加载已下载的单词列表"""
    if not os.path.exists(DOWNLOADED_FILE):
        return set()
    with open(DOWNLOADED_FILE, 'r') as f:
        return set(line.strip() for line in f)

def save_downloaded_word(word):
    """保存已下载的单词"""
    with open(DOWNLOADED_FILE, 'a') as f:
        f.write(f"{word}\n")

def download_pronunciation(word):
    """下载单词发音"""
    for attempt in range(RETRY_TIMES):
        try:
            # 检查是否已存在
            if os.path.exists(f"wordsounds/{word}.mp3"):
                return True
                
            # 剑桥词典URL
            url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 获取发音URL
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            sound_element = soup.find('source', {'type': 'audio/mpeg'})
            
            if not sound_element:
                print(f"[尝试 {attempt+1}/{RETRY_TIMES}] 找不到 {word} 的发音")
                continue
                
            sound_url = sound_element['src']
            if not sound_url.startswith('http'):
                sound_url = 'https://dictionary.cambridge.org' + sound_url
                
            # 下载发音文件
            os.makedirs('wordsounds', exist_ok=True)
            sound_data = requests.get(sound_url, headers=headers, timeout=10).content
            with open(f'wordsounds/{word}.mp3', 'wb') as f:
                f.write(sound_data)
            
            # 保存成功记录
            save_downloaded_word(word)
            return True
            
        except Exception as e:
            print(f"[尝试 {attempt+1}/{RETRY_TIMES}] 下载 {word} 发音失败: {str(e)}")
            time.sleep(random.uniform(1, 3))  # 失败后延迟
    
    return False

def get_all_words():
    """获取所有年级的单词"""
    all_words = set()
    
    # 合并所有年级单词
    for word_data in grade1_words + grade2_words + grade3_words:
        all_words.add(word_data["word"].lower())
    
    return sorted(all_words)

def download_task(word, index, total):
    """单个下载任务"""
    print(f"正在下载 ({index}/{total}): {word}")
    success = download_pronunciation(word)
    return word, success

if __name__ == '__main__':
    # 获取所有单词并过滤已下载的
    all_words = get_all_words()
    downloaded = load_downloaded_words()
    words_to_download = [w for w in all_words if w not in downloaded]
    
    print(f"总单词数: {len(all_words)}, 待下载: {len(words_to_download)}, 已下载: {len(downloaded)}")
    
    # 多线程下载
    success_count = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, word in enumerate(words_to_download, 1):
            futures.append(executor.submit(
                download_task, word, i, len(words_to_download)
            ))
        
        for future in as_completed(futures):
            word, success = future.result()
            if success:
                success_count += 1
    
    print(f"下载完成! 成功下载 {success_count}/{len(words_to_download)} 个单词发音")