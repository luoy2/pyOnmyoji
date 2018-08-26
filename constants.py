from serpent.game import Game
from serpent.input_controller import InputController, InputControllers
import random
import pyautogui

pyautogui.FAILSAFE = False
TIRED_SCALE = None
TIRED_LIMIT = None
WINDOW_OFFSET = None
WINDOW_ATTRIBUTES = {}
INPUT_CONTROLLER = None


def init_constants(game_title=u'阴阳师-网易游戏', move_window=False):
    global TIRED_SCALE
    global TIRED_LIMIT
    global WINDOW_OFFSET
    global INPUT_CONTROLLER
    global WINDOW_ATTRIBUTES
    config = {'window_name': game_title}
    onmyoji_game = Game(window_name=config['window_name'], move_window=move_window)
    WINDOW_ATTRIBUTES = onmyoji_game.after_launch()
    WINDOW_OFFSET = [WINDOW_ATTRIBUTES['x_offset']-12, WINDOW_ATTRIBUTES['y_offset']-47,
                     WINDOW_ATTRIBUTES['width']+WINDOW_ATTRIBUTES['x_offset'],
                     WINDOW_ATTRIBUTES['height']+WINDOW_ATTRIBUTES['y_offset']]
    INPUT_CONTROLLER = InputController(backend=InputControllers.NATIVE_WIN32, game=onmyoji_game)
    TIRED_SCALE = 1
    TIRED_LIMIT = random.random()*100