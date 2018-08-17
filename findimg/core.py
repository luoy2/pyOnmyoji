import pyautogui
from grabscreen import grab_screen
from PIL import Image, ImageEnhance
from colors.util import *
import time
import datetime
import constants
from controller import click
import logging
import utilities



#TODO
# 1. 找色器
# 2. 多点找色
def match_color(img, x, y, expectedRGBColor, tolerance=0):
    pix = img.getpixel((x, y))
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



def find_color(color):
    region = color.region
    region_img = Image.fromarray(grab_screen(region=region), mode='RGB')
    # region_img.show()
    img_size = region_img.size
    for x in range(img_size[0]-1):
        for y in range(img_size[1]-1):
            this_match = True
            for single_color in color.color_list:
                try:
                    if not match_color(region_img, x+single_color[0][0], y+single_color[0][1], single_color[1], color.tolerance):
                        this_match = False
                        break
                except IndexError:
                    pass
            if this_match:
                return (region[0]+x, region[1]+y)
    return None

def myFindColor(color):
    accept_invite()
    return find_color(color)

def accept_invite():
    invite_cords = find_color(UtilColor.AcceptInvite)
    if invite_cords:
        click(invite_cords, 5, tired_check=True)



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
        click(location, rand_offset, tired_check=False)
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
    while color_location:
        click_location = location if location else color_location
        time.sleep(0.2)
        if clicking:
            utilities.random_sleep(clicking_gap, 0.2)
            click(click_location, rand_offset, tired_check=False)
            count += 1
            if count > max_click_time:
                logging.info(f'failed to leave state {img} for {retry_time}.')
                raise Exception
        color_location = myFindColor(color)
        if (datetime.datetime.now() - cur_time).seconds > max_waiting_time:
            logging.info(f'time out finding color table {color}.')
            raise Exception
