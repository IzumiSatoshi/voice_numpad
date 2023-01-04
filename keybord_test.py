import keyboard
import time


def release_callback(e):
    global is_pressing_hotkey
    if is_pressing_hotkey:
        print("release")
    is_pressing_hotkey = False
