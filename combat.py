from findimg.core import *
from controller import click
import logging
import img
import utilities
import enum
from colors.util import CombatColor


class CombatResult(enum.Enum):
    WIN = 'win'
    LOSE = 'fail'


class CombatTimeOutERROR(Exception):
    pass



class Combat:
    def __init__(self, name, mark_loc=None, hero=None, combat_time_limit=300):
        self.result=None
        self.mark_loc=mark_loc
        self.hero=hero
        self.combat_time_limit = combat_time_limit
        self.logger = logging.getLogger('combat')
        self.logger.info(f'开始{name}战斗')


    def start(self, auto_ready=False):
        if not auto_ready:
            ready_loc = wait_for_state(img.combat_img.NOT_READY)
            click(ready_loc, random_range=10, tired_check=False)
        #TODO: AUTO DETECT READY
        return self.get_result()

    def get_result(self):
        # wait_for_color(CombatColor.InCombat)
        win_loc = myFindColor(CombatColor.Win)
        lose_loc = myFindColor(CombatColor.Lose)
        cur_time = datetime.datetime.now()
        while not win_loc and not lose_loc:
            time.sleep(0.3)
            win_loc = myFindColor(CombatColor.Win)
            lose_loc = myFindColor(CombatColor.Lose)
            # self.logger.debug(f'win_loc: {win_loc}; lose_loc: {lose_loc}')
            if (datetime.datetime.now() - cur_time).seconds > self.combat_time_limit:
                self.logger.debug('time out ending combat.')
                raise TimeoutError
        if win_loc:
            click((798, 337), random_range=30, tired_check=False)
            wait_for_leaving_color(CombatColor.Win,
                                   max_waiting_time=15,
                                   max_click_time=5,
                                   clicking=False,
                                   clicking_gap=0.3,
                                   location=(798, 337),
                                   rand_offset=30)
            result = None
            while not result:
                click((57, 940), random_range=3)
                utilities.random_sleep(0.2, 0.5)
                result = myFindColor(CombatColor.Damo)
            wait_for_leaving_color(CombatColor.Damo,
                                   max_waiting_time=15,
                                   max_click_time=3,
                                   clicking=True,
                                   clicking_gap=0.5,
                                   location=(57, 940),
                                   rand_offset=20)
            utilities.random_sleep(1, 2)
            return CombatResult.WIN
        elif lose_loc:
            click((798, 337), random_range=30, tired_check=False)
            wait_for_leaving_color(CombatColor.Lose,
                                   max_waiting_time=15,
                                   max_click_time=3,
                                   clicking=False,
                                   clicking_gap=0.5,
                                   location=(798, 337),
                                   rand_offset=30)
            utilities.random_sleep(1, 2)
            return CombatResult.LOSE
        else:
            self.exist()
            return CombatResult.LOSE
            # raise CombatTimeOutERROR()


    def exist(self):
        click((63, 90), tired_check=False)
        confirm_loc = wait_for_state(img.utilities_img.CONFIRM)
        click(confirm_loc, tired_check=False)
        self.get_result()





if __name__ == '__main__':

    import logging
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    #
    constants.init_constants(u'[#] 阴阳师-网易游戏 [#]', move_window=False)
    self = Combat('test')