from findimg.core import *
import pyautogui
import win32com.client
import time
from serpent.game import Game


TIRED_SCALE = None
TIRED_LIMIT = None
WINDOW_OFFSET = None
INPUT_CONTROLLER = None



if __name__ == '__main__':
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

    constants.init_constants(u'阴阳师-网易游戏', move_window=1)
    while 1:
     result = find_color(ChaoGuiColor.FindChaoGui)
     if result:
         pyautogui.click((510, 392))
         speaker = win32com.client.Dispatch("SAPI.SpVoice")
         speaker.Speak(u"Found Guiwang")
         pyautogui.click((510, 392))
     time.sleep(0.1)

