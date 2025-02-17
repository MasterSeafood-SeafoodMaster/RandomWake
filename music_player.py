import os
import random
import pygame
from tkinter import messagebox
from config import MUSIC_FOLDER

# 初始化 pygame 音樂播放器
pygame.mixer.init()

# 播放隨機音樂
def play_random_music():
    # 確認音樂資料夾是否存在
    if not os.path.exists(MUSIC_FOLDER):
        messagebox.showerror("錯誤", f"資料夾 {MUSIC_FOLDER} 不存在！")
        return

    # 取得資料夾中的所有音樂檔案
    music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3') or f.endswith('.wav')]
    if not music_files:
        messagebox.showerror("錯誤", "資料夾中沒有音樂檔案！")
        return

    # 隨機選擇一首音樂
    chosen_song = random.choice(music_files)
    song_path = os.path.join(MUSIC_FOLDER, chosen_song)

    # 播放音樂並循環
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(-1)  # -1 代表循環播放

    return chosen_song

# 停止音樂播放
def stop_music():
    pygame.mixer.music.stop()
