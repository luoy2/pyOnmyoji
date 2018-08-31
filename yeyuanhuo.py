import constants
from controller import click
from combat import Combat, CombatResult
from findimg import *
import pytesseract
from colors.util import PartyColor
import img
import parties
import time
import utilities
import multiprocessing

class YeyuanhuoColor:
    ChooseYeyuanhuo = ColorToMatch([1140, 440, 1180, 520], [[(0, 0), (249, 243, 252)], [(-53, 50), (44, 168, 141)], [(-1, 127), (84, 67, 80)]], 1)
    ReadyFightYeyuanhuoChi = ColorToMatch([1252, 684, 1357, 758], [[(0, 0), (243, 178, 94)], [(36, -27), (152, 61, 46)], [(-286, -252), (242, 250, 249)]], 1)


YeyuanhuoOCRLocation = {
    "CHI": [1040, 68, 1099, 99],
}

class YeyuanhuoFighter:
    def __init__(self, type="CHI"):
        self.type = type
        self.logger = logging.getLogger(__name__)

    def get_remain_chance(self):
        cords = YeyuanhuoOCRLocation[self.type]
        x1, y1, x2, y2 = cords
        x1, y1 = cordinates_convert((x1, y1), constants.WINDOW_ATTRIBUTES)
        x2, y2 = cordinates_convert((x2, y2), constants.WINDOW_ATTRIBUTES)
        img = grab_screen([x1, y1, x2, y2])
        img = Image.fromarray(img)
        remain = int(pytesseract.image_to_string(img, config='-psm 6').replace('O', '0'))
        self.logger.debug(f'remaining chance: {remain}')
        return remain

    def start(self):
        enter_yeyuanhuo()
        while self.get_remain_chance():
            fight_loc = wait_for_color(YeyuanhuoColor.ReadyFightYeyuanhuoChi, max_time=10)
            click(fight_loc, random_range=5, tired_check=True)
            utilities.random_sleep(90, 60*3)
            wait_for_color(CombatColor.Damo, max_time=60*5)
            leaving_test = 0
            while leaving_test < 3:
                utilities.random_sleep(0.2, 0.5)
                wait_for_leaving_color(CombatColor.Damo,
                                       max_waiting_time=15,
                                       max_click_time=8,
                                       clicking=True,
                                       clicking_gap=0.2,
                                       location=(57, 940),
                                       rand_offset=20)
                leaving_test += 1



def enter_yeyuanhuo():
    pass



def main_yeyuanhuo():
    fighter = YeyuanhuoFighter()
    fighter.start()


if __name__ == '__main__':
    import constants
    import logging
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")

    # constants.init_constants(u'阴阳师-网易游戏', move_window=True)
    # as_leader('御魂')

    constants.init_constants(u'阴阳师-网易游戏', move_window=True)
    main_yeyuanhuo()

