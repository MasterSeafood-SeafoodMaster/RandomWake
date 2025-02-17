import tkinter as tk
from tkinter import messagebox
from music_player import play_random_music, stop_music
from utils import get_remaining_time, calculate_alarm_time

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("隨機音樂鬧鐘")
        self.root.geometry("400x300")

        # 預設鬧鐘時間
        self.alarm_datetime = None

        # UI 元素
        self.title_label = tk.Label(root, text="隨機音樂鬧鐘", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.input_label = tk.Label(root, text="請輸入鬧鐘時間 (HH:MM):", font=("Arial", 12))
        self.input_label.pack(pady=10)

        self.alarm_time_entry = tk.Entry(root, font=("Arial", 12))
        self.alarm_time_entry.insert(0, '08:00')  # 預設為 08:00
        self.alarm_time_entry.pack(pady=5)

        self.alarm_time_label = tk.Label(root, text="鬧鐘設置時間：", font=("Arial", 12))
        self.alarm_time_label.pack(pady=10)

        self.countdown_label = tk.Label(root, text="倒數時間: 00:00", font=("Arial", 12))
        self.countdown_label.pack(pady=10)

        self.set_alarm_button = tk.Button(root, text="設置鬧鐘", font=("Arial", 12), command=self.set_alarm)
        self.set_alarm_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.cancel_alarm_button = tk.Button(root, text="取消鬧鐘", font=("Arial", 12), command=self.cancel_alarm, state=tk.DISABLED)
        self.cancel_alarm_button.pack(side=tk.LEFT, padx=20, pady=10)

    def set_alarm(self):
        alarm_time_str = self.alarm_time_entry.get()

        if not alarm_time_str:
            messagebox.showerror("錯誤", "請輸入鬧鐘時間！")
            return

        try:
            self.alarm_datetime = calculate_alarm_time(alarm_time_str)
            self.alarm_time_label.config(text=f"鬧鐘設置時間：{self.alarm_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            self.update_countdown()

            self.set_alarm_button.config(state=tk.DISABLED)
            self.cancel_alarm_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("錯誤", "時間格式錯誤！請使用 HH:MM 格式（24小時制）")

    def cancel_alarm(self):
        self.alarm_datetime = None
        self.countdown_label.config(text="倒數時間: 00:00")
        self.set_alarm_button.config(state=tk.NORMAL)
        self.cancel_alarm_button.config(state=tk.DISABLED)

    def update_countdown(self):
        if self.alarm_datetime:
            remaining_time = get_remaining_time(self.alarm_datetime)

            if remaining_time > 0:
                minutes, seconds = divmod(int(remaining_time), 60)
                self.countdown_label.config(text=f"倒數時間: {minutes:02}:{seconds:02}")
                self.root.after(1000, self.update_countdown)  # 每秒更新
            else:
                self.countdown_label.config(text="鬧鐘時間到了！")
                self.play_alarm()

    def play_alarm(self):
        song = play_random_music()
        self.show_music_modal(song)

    def show_music_modal(self, song):
        modal = tk.Toplevel(self.root)
        modal.title("鬧鐘響起")
        modal.geometry("300x150")

        message_label = tk.Label(modal, text=f"時間到！正在播放 {song}，請享受音樂！", font=("Arial", 12))
        message_label.pack(pady=20)

        confirm_button = tk.Button(modal, text="確認", font=("Arial", 12), command=lambda: self.stop_music_and_cancel_alarm(modal))
        confirm_button.pack(pady=10)

    def stop_music_and_cancel_alarm(self, modal):
        stop_music()
        self.cancel_alarm()
        modal.destroy()
