import random
import cv2
from serpent.input_controller import InputController, InputControllers, KeyboardKey
from serpent.game import Game
import pyautogui
import logging
import time
from main import TIRED_SCALE
from serpent.input_controller import MouseButton


config = {'executable_path':'F:\Onmyoji\Launch.exe', 'window_name':u'阴阳师-网易游戏'}
onmyoji_game=Game(executable_path=config['executable_path'], window_name=config['window_name'])
onmyoji_game.after_launch()
input_controller = InputController(backend=InputControllers.NATIVE_WIN32, game=onmyoji_game)

def click(cords, random_range=5,tired_check=True):
    if tired_check:
        perform_tired_check()
    global input_controller
    global TIRED_SCALE
    x, y=cords
    rand_x = x + random.randrange(-random_range, random_range)
    rand_y = y + random.randrange(-random_range, random_range)
    pyautogui.click(rand_x, rand_y)
    pyautogui.moveTo(rand_x, rand_y)
    TIRED_SCALE += random.random()/2

    # input_controller.move(rand_x, rand_y)
    # input_controller.click(MouseButton.LEFT)

def escape():
    input_controller.tap_key(KeyboardKey.KEY_ESCAPE, duration=0.25+random.random()/10)


def perform_tired_check():
    global TIRED_SCALE
    logging.debug(f'tired scale: {TIRED_SCALE}')
    tired_probablity = TIRED_SCALE/100
    tired = random.random() < tired_probablity
    if tired:
        resting_time = TIRED_SCALE*3
        logging.info(f'resting {resting_time/60} minute...')
        time.sleep(TIRED_SCALE*3)
        TIRED_SCALE = 0