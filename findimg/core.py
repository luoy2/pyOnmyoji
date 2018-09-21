import pyautogui
from grabscreen import grab_screen
from PIL import Image, ImageEnhance
from colors.util import *
import time
import datetime
import constants
from controller import *
import logging
import utilities
import numpy as np


#TODO
# 1. 找色器
# 2. 多点找色
def _match_color(img, x, y, expectedRGBColor, tolerance=0):
    pix = img.getpixel((x, y))
    # pix = img[x][y]
    if len(pix) == 3 or len(expectedRGBColor) == 3:  # RGB mode
        r, g, b = pix[:3]
        exR, exG, exB = expectedRGBColor[:3]
        return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance)
    elif len(pix) == 4 and len(expectedRGBColor) == 4:  # RGBA mode
        r, g, b, a = pix
        exR, exG, exB, exA = expectedRGBColor
        return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance) and (
                    abs(a - exA) <= tolerance)
    else:
        assert False, 'Color mode was expected to be length 3 (RGB) or 4 (RGBA), but pixel is length %s and expectedRGBColor is length %s' % (
        len(pix), len(expectedRGBColor))





from tqdm import *

#
def find_color(color):
    search_region = utilities.add_pos_with_offset(color.region, constants.WINDOW_ATTRIBUTES)
    img_region = utilities.add_pos_with_offset(color.screen_shot_region, constants.WINDOW_ATTRIBUTES)
    screen_shot_img = Image.fromarray(grab_screen(region=img_region), mode='RGB')
    # screen_shot_img = grab_screen(region=img_region).transpose(1,0,2)
    offset_x = search_region[0] - img_region[0]
    offset_y = search_region[1] - img_region[1]
    # region_img = Image.fromarray(grab_screen(region=region), mode='RGB')
    # region_img.show()
    for x in range(search_region[2] - search_region[0] + 1):
        for y in range(search_region[3] - search_region[1] + 1):
            this_match = True
            for single_color in color.color_list:
                try:
                    cords_offset = cordinates_scale((single_color[0][0]+offset_x, single_color[0][1]+offset_y), constants.WINDOW_ATTRIBUTES)
                    if not _match_color(screen_shot_img, x+cords_offset[0], y+cords_offset[1], single_color[1], color.tolerance):
                        this_match = False
                        break
                except IndexError:
                    pass
            if this_match:
                return (search_region[0]+x, search_region[1]+y)
    return None

def myFindColor(color):
    accept_invite()
    return find_color(color)

def delay_find_color(color, delay_gap):
    time.sleep(delay_gap)
    # color.show()
    return myFindColor(color)

def accept_invite():
    invite_cords = find_color(UtilColor.AcceptInvite)
    if invite_cords:
        rand_x = invite_cords[0] + random.randrange(-2, 2)
        rand_y = invite_cords[1] + random.randrange(-2, 2)
        pyautogui.click(rand_x, rand_y)


def if_outof_sushi():
    outsushi_result = myFindColor(UtilColor.OutofSushi)
    if outsushi_result:
        logging.warning('体力不足!')
        exit(0)


def findimg(img, confidence=0.98, grayscale=False):
    accept_invite()
    img_path, img_region = img
    img_region = list(img_region)
    img_region[0] += constants.WINDOW_OFFSET[0]
    img_region[2] += constants.WINDOW_OFFSET[0]
    img_region[1] += constants.WINDOW_OFFSET[1]
    img_region[3] += constants.WINDOW_OFFSET[1]
    location = pyautogui.locateCenterOnScreen(img_path,
                                              grayscale=grayscale,
                                              region=img_region,
                                              confidence=confidence)
    if location:
        return location
    else:
        return None

def findimg_all(img):
    img_path, img_region = img
    logging.debug(f'find all {img_path} in {img_region}')
    img_region = list(img_region)
    img_region[0] += constants.WINDOW_OFFSET[0]
    img_region[2] += constants.WINDOW_OFFSET[0]
    img_region[1] += constants.WINDOW_OFFSET[1]
    img_region[3] += constants.WINDOW_OFFSET[1]
    locations = pyautogui.locateAllOnScreen(img_path,
                                              grayscale=True,
                                              region=img_region)
    if locations:
        return locations
    else:
        return None



def wait_for_leaving_state(img, max_time=5):
    location = findimg(img)
    cur_time = datetime.datetime.now()
    while location:
        time.sleep(0.1)
        location = findimg(img)
        if (datetime.datetime.now() - cur_time).seconds > max_time:
            logging.info(f'time out leaving state {img}.')
            break


def click_to_leaving_state(img, retry_time=10, location=None, rand_offset=10):
    if not location:
        location = findimg(img)
    count = 0
    while location:
        utilities.random_sleep(0.2, 0.4)
        click(location, rand_offset, tired_check=False, need_convert=True)
        count += 1
        location = findimg(img)
        if count > retry_time:
            logging.info(f'failed to leave state {img} for {retry_time}.')
            break

def click_to_get_state(img, location, retry_time=10, rand_offset=10, grayscale=True):
    count = 0
    img_loc = findimg(img, grayscale=grayscale)
    while not img_loc:
        time.sleep(0.2)
        click(location, rand_offset, tired_check=False)
        count += 1
        img_loc = findimg(img)
        if count > retry_time:
            logging.info(f'failed to get state {img} for {retry_time}.')
            break


def wait_for_state(img, max_time=15, confidence=0.98, grayscale=False):
    logging.info(f'trying to find img {img[0]} at region {img[1]}')
    location = findimg(img)
    cur_time = datetime.datetime.now()
    while not location:
        time.sleep(0.1)
        location = findimg(img, confidence, grayscale)
        if (datetime.datetime.now() - cur_time).seconds > max_time:
            logging.info(f'time out finding img {img[0]} at region {img[1]}.')
            break
    return location


def wait_for_color(color, max_time=15):
    logging.info(f'trying to find color table {color}')
    location = myFindColor(color)
    cur_time = datetime.datetime.now()
    while not location:
        time.sleep(0.2)
        location = myFindColor(color)
        if (datetime.datetime.now() - cur_time).seconds > max_time:
            logging.info(f'time out finding color table {color}.')
            break
    return location


def wait_for_leaving_color(color,
                           max_waiting_time=15,
                           max_click_time=5,
                           clicking=False,
                           clicking_gap=0.2,
                           location=None,
                           rand_offset=3):
    logging.info(f'trying to leave color table {color}')
    color_location = myFindColor(color)
    count = 0
    cur_time = datetime.datetime.now()
    recheck = 0
    while recheck < 3:
        while color_location:
            click_location = location if location else color_location
            time.sleep(0.2)
            if clicking:
                utilities.random_sleep(clicking_gap, 0.2)
                click(click_location, rand_offset, tired_check=False, need_convert=True)
                count += 1
                if count > max_click_time:
                    logging.info(f'failed to leave state {img} for {retry_time}.')
                    raise Exception
            time.sleep(0.5)
            color_location = myFindColor(color)
            if (datetime.datetime.now() - cur_time).seconds > max_waiting_time:
                logging.info(f'time out finding color table {color}.')
                raise Exception
        recheck+=1
    time.sleep(0.5)



def map_locator():
    max_retry_time = 3*60
    cur_time = datetime.datetime.now()
    while 1:
        for i in [LocatorColor.Map, LocatorColor.Main, LocatorColor.Jiejie]:
            _ = myFindColor(i)
            if _:
                logging.debug('found map color.. now confirm')
                for retry in range(3):
                    retry_color = myFindColor(i)
                    if not retry_color:
                        logging.debug('confirm failed')
                        return map_locator()
                return i
        time.sleep(3)
        logging.debug("didn't find any map color.")
        if  (datetime.datetime.now()-cur_time).total_seconds() > max_retry_time:
            logging.debug('map color finder timeout')
            raise TimeoutError