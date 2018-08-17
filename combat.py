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
        wait_for_color(CombatColor.InCombat)
        wait_for_leaving_color(CombatColor.InCombat, max_waiting_time=self.combat_time_limit)
        win_loc = findimg(img.combat_img.WIN)
        lose_loc = findimg(img.combat_img.LOSE)
        cur_time = datetime.datetime.now()
        while not win_loc and not lose_loc:
            time.sleep(0.3)
            win_loc = findimg(img.combat_img.WIN)
            lose_loc = findimg(img.combat_img.LOSE)
            # self.logger.debug(f'win_loc: {win_loc}; lose_loc: {lose_loc}')
            if (datetime.datetime.now() - cur_time).seconds > 10:
                self.logger.debug('time out ending combat.')
                raise TimeoutError
        if win_loc:
            click_to_leaving_state(img.combat_img.WIN, rand_offset=50, location=win_loc)
            result_loc = wait_for_state(img.combat_img.RESULT2, 100)
            click_to_leaving_state(img.combat_img.RESULT2, rand_offset=100, location=result_loc)
            utilities.random_sleep(1, 2)
            return CombatResult.WIN
        elif lose_loc:
            click_to_leaving_state(img.combat_img.LOSE, rand_offset=50, location=lose_loc)
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
    combat = Combat('结界突破')
    combat_result = combat.start(True)
    combat.exist()