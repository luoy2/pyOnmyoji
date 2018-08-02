import win32api
import constants
import img
from party import main_yaoqi
from ctypes import windll
from grabscreen import grab_screen

import logging

user32 = windll.user32
user32.SetProcessDPIAware()

import os
from multiprocessing import Process
constants.init_constants()
logging.basicConfig(
    level=0,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")






#
target_monster = img.ss_img.RIHEFANG
count = 30
main_yaoqi(count, img.ss_img.RIHEFANG)