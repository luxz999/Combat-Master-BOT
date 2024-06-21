import pyautogui
import time

def get_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"mouse position: x={x}, y={y}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")


get_mouse_position()