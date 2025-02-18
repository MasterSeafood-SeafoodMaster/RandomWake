import tkinter as tk
from tkinter import messagebox
import ctypes  # 用於喚醒電腦
from music_player import play_random_music, stop_music
from utils import get_remaining_time, calculate_alarm_time
from config import FONT  # Import font from config.py

LARGE_FONT = (FONT[0], 16, FONT[2])
BUTTON_FONT = (FONT[0], 14, FONT[2])

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Music Alarm")
        self.root.geometry("500x350")
        self.root.configure(bg="white")

        self.alarm_datetime = None

        self.title_label = tk.Label(root, text="Random Music Alarm", font=(FONT[0], 20, "bold"), bg="white")
        self.title_label.pack(pady=15)

        self.input_label = tk.Label(root, text="Enter alarm time (HH:MM):", font=LARGE_FONT, bg="white")
        self.input_label.pack(pady=10)

        self.alarm_time_entry = tk.Entry(root, font=LARGE_FONT, width=10, justify='center')
        self.alarm_time_entry.insert(0, '08:00')
        self.alarm_time_entry.pack(pady=5)

        self.alarm_time_label = tk.Label(root, text="Alarm Set Time:", font=LARGE_FONT, bg="white")
        self.alarm_time_label.pack(pady=10)

        self.countdown_label = tk.Label(root, text="Countdown: 00:00", font=LARGE_FONT, bg="white")
        self.countdown_label.pack(pady=10)

        self.button_frame = tk.Frame(root, bg="white")
        self.button_frame.pack(pady=10)

        self.set_alarm_button = tk.Button(self.button_frame, text="Set Alarm", font=BUTTON_FONT, command=self.set_alarm)
        self.set_alarm_button.pack(side=tk.LEFT, padx=15, pady=5)

        self.cancel_alarm_button = tk.Button(self.button_frame, text="Cancel Alarm", font=BUTTON_FONT, command=self.cancel_alarm, state=tk.DISABLED)
        self.cancel_alarm_button.pack(side=tk.LEFT, padx=15, pady=5)

    def set_alarm(self):
        alarm_time_str = self.alarm_time_entry.get()
        if not alarm_time_str:
            messagebox.showerror("Error", "Please enter an alarm time!")
            return

        try:
            self.alarm_datetime = calculate_alarm_time(alarm_time_str)
            self.alarm_time_label.config(text=f"Alarm Set Time: {self.alarm_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            self.update_countdown()
            self.set_alarm_button.config(state=tk.DISABLED)
            self.cancel_alarm_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Error", "Invalid time format! Please use HH:MM (24-hour format)")

    def cancel_alarm(self):
        self.alarm_datetime = None
        self.alarm_time_label.config(text="Alarm Set Time:")
        self.countdown_label.config(text="Countdown: 00:00")
        self.set_alarm_button.config(state=tk.NORMAL)
        self.cancel_alarm_button.config(state=tk.DISABLED)


    def update_countdown(self):
        if self.alarm_datetime:
            remaining_time = get_remaining_time(self.alarm_datetime)
            if remaining_time > 0:
                minutes, seconds = divmod(int(remaining_time), 60)
                self.countdown_label.config(text=f"Countdown: {minutes:02}:{seconds:02}")
                self.root.after(1000, self.update_countdown)
            else:
                self.countdown_label.config(text="Time's up!")
                self.wake_up_computer()
                self.play_alarm()

    def wake_up_computer(self):
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # 喚醒電腦並防止進入睡眠
        except Exception as e:
            print(f"Error waking up computer: {e}")

    def play_alarm(self):
        song = play_random_music()
        self.show_music_modal(song)

    def show_music_modal(self, song):
        modal = tk.Toplevel(self.root)
        modal.title("Alarm Ringing")
        modal.geometry("350x200")
        modal.configure(bg="white")

        message_label = tk.Label(modal, text=f"Time's up! Now playing {song}. Enjoy the music!", font=LARGE_FONT, bg="white", wraplength=300)
        message_label.pack(pady=20)

        confirm_button = tk.Button(modal, text="OK", font=BUTTON_FONT, command=lambda: self.stop_music_and_cancel_alarm(modal))
        confirm_button.pack(pady=10)

    def stop_music_and_cancel_alarm(self, modal):
        stop_music()
        self.cancel_alarm()
        modal.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
