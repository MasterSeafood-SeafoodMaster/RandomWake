import tkinter as tk
from alarm_ui import AlarmApp

def main():
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
