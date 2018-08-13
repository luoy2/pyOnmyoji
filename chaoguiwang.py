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
    config = {'executable_path': '', 'window_name': u'阴阳师-网易游戏'}
    onmyoji_game = Game(executable_path=config['executable_path'], window_name=config['window_name'])
    onmyoji_game.after_launch()
    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    while 1:
     result = find_color(ChaoGuiColor.FindChaoGui)
     if result:
         speaker = win32com.client.Dispatch("SAPI.SpVoice")
         speaker.Speak(u"Found Guiwang！")
         pyautogui.click((510, 392))
     time.sleep(0.5)

