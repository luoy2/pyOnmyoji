import win32api
import win32con
import win32gui
from PIL import ImageGrab, Image
import numpy as np
import cv2
import time
import random
from ctypes import windll
from grabscreen import grab_screen
from serpent.game import Game
from serpent.input_controller import InputController, InputControllers
import pyautogui
user32 = windll.user32
user32.SetProcessDPIAware()

import os
from multiprocessing import Process

TIRED_SCALE = 1



def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)




    # last_time = time.time()
    # while(True):
    #     # 800x600 windowed mode
    #     printscreen = np.array(ImageGrab.grab(bbox=screen_box_size))
    #     print('loop took {} seconds'.format(time.time()-last_time))
    #     last_time = time.time()
    #     cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         cv2.destroyAllWindows()
    #         break


def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    return processed_img

def get_hash(img):
    img = img.resize((16, 16), Image.ANTIALIAS).convert('L')  # 抗锯齿 灰度
    avg = sum(list(img.getdata())) / 256  # 计算像素平均值
    s = ''.join(map(lambda i: '0' if i < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
    return ''.join(map(lambda j: '%x' % int(s[j:j+4], 2), range(0, 256, 4)))



def hamming(hash1, hash2, n=20):
    b = False
    assert len(hash1) == len(hash2)
    if sum([ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)]) < n:
        b = True
    return b


def screen_record():
    last_time = time.time()
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    while True:
        window_size = get_window_info()
        # screen = np.array(ImageGrab.grab(bbox=window_size))
        screen = np.array(grab_screen(region=window_size))
        # print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        # new_screen = process_img(screen)
        imS = cv2.resize(screen, (1980, 1080))
        cv2.imshow('output', imS)
        # cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

