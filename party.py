import constants
from controller import click
from combat import Combat, CombatResult
from findimg import *
from colors.util import PartyColor
import img
import parties
import time
import utilities
import multiprocessing

def main_yaoqi(times, target_monster):
    count = 0
    while count < times:
        yaoqi_loc = wait_for_state(img.party_img.YAOQIFENGYIN)
        click(yaoqi_loc)

        refresh_location = wait_for_state(img.party_img.REFRESH)
        parties.yaoqifengyin.find_monster(target_monster, refresh_location)

        combat = Combat('妖气封印')
        combat_result = combat.start()

        party_loc = wait_for_state(img.party_img.MAIN_PARTY, 15)
        time.sleep(1)
        click_to_leaving_state(img.party_img.MAIN_PARTY, rand_offset=10, location=party_loc)

        count += 1

def as_member(batter_name):
    while 1:
        battle = Combat(batter_name)
        battle.start(auto_ready=True)
        time.sleep(2)

def as_leader(batter_name):
    while 1:
        battle = Combat(batter_name)
        battle.start(auto_ready=True)
        time.sleep(2)
        start_loc = wait_for_color(PartyColor.StartFight)
        utilities.random_sleep(0.5, 2)
        click(start_loc, random_range=3, tired_check=True)

if __name__ == '__main__':
    import constants
    import combat
    import logging
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    #
    constants.init_constants(u'阴阳师-网易游戏', move_window=False)
    # constants.init_constants(u'阴阳师-网易游戏', move_window=False)
    as_leader('御魂')

    # constants.init_constants(u'[#] 阴阳师-网易游戏 [#]', move_window=True)
    # as_member('御魂')


# if __name__ == '__main__':
#     import constants
#     import combat
#     import logging
#     from ctypes import windll
#
#     user32 = windll.user32
#     user32.SetProcessDPIAware()
#
#     constants.init_constants(u'[#] 阴阳师-网易游戏 [#]')
#     logging.basicConfig(
#         level=0,
#         format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
#         datefmt="%Y-%m-%d %H:%M:%S")
