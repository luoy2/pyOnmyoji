import pyautogui
import time
import datetime
import constants
from controller import click
import logging


class ImgNotFound(Exception):
    pass

def findimg(img):
    img_path, img_region = img
    img_region = list(img_region)
    img_region[0] += constants.WINDOW_OFFSET[0]
    img_region[2] += constants.WINDOW_OFFSET[0]
    img_region[1] += constants.WINDOW_OFFSET[1]
    img_region[3] += constants.WINDOW_OFFSET[1]
    location = pyautogui.locateCenterOnScreen(img_path,
                                              grayscale=True,
                                              region=img_region)
    if location:
        return location
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
            raise ImgNotFound()
            # break


def click_to_leaving_state(img, retry_time=10, location=None, rand_offset=10):
    if not location:
        location = findimg(img)
    count = 0
    while location:
        time.sleep(0.2)
        click(location, rand_offset, tired_check=False)
        count += 1
        location = findimg(img)
        if count > retry_time:
            logging.info(f'failed to leave state {img} for {retry_time}.')
            raise ImgNotFound()
            # break


def wait_for_state(img, max_time=15):
    logging.info(f'trying to find img {img[0]} at region {img[1]}')
    location = findimg(img)
    cur_time = datetime.datetime.now()
    while not location:
        time.sleep(0.1)
        location = findimg(img)
        if (datetime.datetime.now() - cur_time).seconds > max_time:
            logging.info(f'time out finding img {img[0]} at region {img[1]}.')
            raise ImgNotFound()
            # break
    return location

