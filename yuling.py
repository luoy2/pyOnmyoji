import constants
from controller import click
from combat import Combat, CombatResult
from findimg import *
import pytesseract
from colors.util import PartyColor
import img
import parties
import time
import combat
import utilities
import multiprocessing

class YuLinColor:
    ChooseYuLin = ColorToMatch([1140, 440, 1180, 520], [[(0, 0), (249, 243, 252)], [(-53, 50), (44, 168, 141)], [(-1, 127), (84, 67, 80)]], 1)
    ReadyFightYuLinChi = ColorToMatch([1237, 677, 1340, 738], [[(0, 0), (243, 178, 94)], [(77, -30), (152, 61, 46)], [(75, 36), (151, 60, 46)]], 1)


YuLinOCRLocation = {
    "REMAIN": [1297, 68, 1360, 100],
}

class YuLinFighter:
    def __init__(self, type="REMAIN"):
        self.type = type
        self.logger = logging.getLogger(__name__)

    def get_remain_chance(self):
        cords = YuLinOCRLocation[self.type]
        x1, y1, x2, y2 = cords
        x1, y1 = cordinates_convert((x1, y1), constants.WINDOW_ATTRIBUTES)
        x2, y2 = cordinates_convert((x2, y2), constants.WINDOW_ATTRIBUTES)
        img = grab_screen([x1, y1, x2, y2])
        img = Image.fromarray(img)
        remain = int(pytesseract.image_to_string(img, config='-psm 6').replace('O', '0'))
        self.logger.debug(f'remaining chance: {remain}')
        return remain

    def start(self):
        enter_yulin()
        while self.get_remain_chance():
            fight_loc = wait_for_color(YuLinColor.ReadyFightYuLinChi, max_time=10)
            click(fight_loc, random_range=5, tired_check=True)
            this_fight = combat.Combat('御灵', combat_time_limit=60 * 5 + random.randint(40, 80))
            combat_result = this_fight.start(auto_ready=True)



def enter_yulin():
    pass



def main_yulin():
    fighter = YuLinFighter()
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
    main_yulin()

