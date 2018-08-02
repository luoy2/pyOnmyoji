import win32api
import constants
import img
from party import main_yaoqi
from ctypes import windll
from findimg import *
import datetime
import pyautogui
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



def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

from controller import *
from constants import *

def gather_gamble_data():
    logging.info('gathering gambling data...')
    #1. 点击青蛙
    file_name = datetime.datetime.now().strftime('%Y%m%d_%H.png')
    gamble_title = wait_for_state(img.gamble_img.GAMBLE_MAIN)
    click((gamble_title[0], gamble_title[1]+133), random_range=10, tired_check=False)
    wait_for_state(img.gamble_img.GAMBLE_DASH)

    #2. 点击桌边面板， 截图
    click((348, 261), random_range=20, tired_check=False)
    INPUT_CONTROLLER.move(1200, 0)
    wait_for_state(img.gamble_img.RED)
    pyautogui.screenshot('data/gamble/red/' + file_name, region=WINDOW_OFFSET)
    time.sleep(2)


    #3. 点击右边面板， 截图
    click((1085, 643), tired_check=False)
    INPUT_CONTROLLER.move(1200, 0)
    wait_for_state(img.gamble_img.BLUE)
    pyautogui.screenshot('data/gamble/blue/' + file_name, region=WINDOW_OFFSET)
    time.sleep(2)

    #4. 点击红叉
    exist_loc = wait_for_state(img.utilities_img.RED_CROSS)
    click(exist_loc, tired_check=False)
    time.sleep(1)

    #5. 竞猜
    click((300, 459), tired_check=False)
    time.sleep(2)
    click((951, 453), random_range=20, tired_check=False)
    time.sleep(2)
    exist_loc = wait_for_state(img.utilities_img.RED_CROSS)
    click(exist_loc, tired_check=False)


    #6. 等待2小时, 获取结果， 进行下一次竞猜
    time.sleep(3600*2)
    logging.debug('sleeping...')
    gamble_title = wait_for_state(img.gamble_img.GAMBLE_MAIN)
    click((gamble_title[0], gamble_title[1]+133), random_range=10, tired_check=False)
    wait_for_state(img.gamble_img.GAMBLE_DASH)
    pyautogui.screenshot('data/gamble/result/' + file_name, region=WINDOW_OFFSET)
    for i in range(5):
        click((570, 219), random_range=20)
        time.sleep(1)

    next = wait_for_state(img.gamble_img.NEXT)
    click(next, tired_check=False)
    exist_loc = wait_for_state(img.utilities_img.RED_CROSS)
    click(exist_loc, tired_check=False)


if __name__ == '__main__':
    while 1:
        gather_gamble_data()