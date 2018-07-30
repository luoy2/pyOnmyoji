import random
from serpent.input_controller import InputController, InputControllers, KeyboardKey
import pyautogui
import logging
import constants
import time



def click(cords, random_range=5,tired_check=True):
    if tired_check:
        perform_tired_check()
    x, y=cords
    rand_x = x + random.randrange(-random_range, random_range)
    rand_y = y + random.randrange(-random_range, random_range)
    pyautogui.click(rand_x, rand_y)
    pyautogui.moveTo(rand_x, rand_y)
    constants.TIRED_SCALE += random.random()/2

    # input_controller.move(rand_x, rand_y)
    # input_controller.click(MouseButton.LEFT)

def escape():
    constants.INPUT_CONTROLLER.tap_key(KeyboardKey.KEY_ESCAPE, duration=0.25+random.random()/10)


def perform_tired_check():
    logging.debug(f'tired scale: {constants.TIRED_SCALE}/{constants.TIRED_LIMIT}')
    tired = constants.TIRED_SCALE > constants.TIRED_LIMIT
    if tired:
        resting_time = constants.TIRED_SCALE*3
        logging.info(f'resting {resting_time/60} minute...')
        time.sleep(constants.TIRED_SCALE*3)
        constants.TIRED_SCALE = 1
        constants.TIRED_LIMIT = random.random()*100