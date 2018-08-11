import win32api
import constants
import img
from party import main_yaoqi
from ctypes import windll
from grabscreen import grab_screen
from jiejietupo import *

import logging





def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)



#
# target_monster = img.ss_img.HAIFANGZHU
# count = 4
# main_yaoqi(count, target_monster)
#
if __name__ == '__main__':
    user32 = windll.user32
    user32.SetProcessDPIAware()
    constants.init_constants()
    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    main_all_tupo(3, True)