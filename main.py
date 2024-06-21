import pyautogui
import json
import time
import pygetwindow
import tkinter as tk
from tkinter import messagebox, ttk
import threading

config = json.load(open("config.json"))
duration = config['duration'].replace('m', '')

running = False

def switch_to_combat_master():
    windows = pygetwindow.getWindowsWithTitle('Combat Master')
    if windows:
        print(f"Switching to Combat Master")
        windows[0].activate()
        return True
    else:
        print("Combat Master not found")
        messagebox.showerror("Error", "Combat Master window not found. Stopping the bot.")
        return False

def bot_loop():
    global running
    try:
        while running:
            if not switch_to_combat_master():
                running = False
                update_status()
                toggle_button.config(text="Start Bot", command=start_bot)
                return
            time.sleep(0.7)
            pyautogui.click(x=config['start_match']['x'], y=config['start_match']['y'])
            time.sleep(int(duration) * 60 + 20)
            if not switch_to_combat_master():
                running = False
                update_status()
                toggle_button.config(text="Start Bot", command=start_bot)
                return
            time.sleep(0.7)
            pyautogui.click(x=config['back_to_game_room']['x'], y=config['back_to_game_room']['y'])
            time.sleep(0.7)
    except KeyboardInterrupt:
        print("Program stopped")

def update_status():
    if running:
        status_label.config(text="Bot is running", foreground="green")
    else:
        status_label.config(text="Bot is stopped", foreground="red")

def start_bot():
    global running
    if duration not in ['3', '5', '8', '13']:
        messagebox.showerror("Error", "Invalid duration")
        root.destroy()
    else:
        running = True
        toggle_button.config(text="Stop Bot", command=stop_bot)
        update_status()
        bot_thread = threading.Thread(target=bot_loop)
        bot_thread.start()

def stop_bot():
    global running
    running = False
    toggle_button.config(text="Start Bot", command=start_bot)
    update_status()
    print("Bot stopped")

root = tk.Tk()
root.title("Combat Master Bot")
root.geometry("300x250")

root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12), padding=5)
label = ttk.Label(root, text="Combat Master Bot", style="TLabel")
label.pack(pady=10)

status_label = ttk.Label(root, text="Bot is stopped", style="TLabel", foreground="red")
status_label.pack(pady=10)

toggle_button = ttk.Button(root, text="Start Bot", command=start_bot, style="TButton")
toggle_button.pack(pady=5)


root.mainloop()