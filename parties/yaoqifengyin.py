from controller import *
from findimg import *
from utilities import *
from img.party_img import *
from img.utilities_img import *
import img
from findimg import *
import random

def waiting_for_refreshing():
    while pyautogui.pixelMatchesColor(1030, 543, (255, 255, 255)):
        time.sleep(0.1)


def enter_yaoqi_party(loc):
    x, y = loc
    enter_x = x+665
    enter_y = y+32
    click((enter_x, enter_y), tired_check=False)
    # wait_for_leaving_state(REFRESH_WAITING)
    random_sleep()
    time.sleep(1+random.random())
    if findimg(NOT_ENOUGH_SUSHI):
        escape()
        exit(0)
    if not findimg(REFRESH):
        print('进入队伍成功！')
        return True
    else:
        print('进入队伍失败！')
        return False


def find_monster(target_monster, refresh_location):
    monster_loc = findimg(target_monster)
    while not monster_loc:
        click(refresh_location)
        # wait_for_leaving_state(REFRESH_WAITING)
        waiting_for_refreshing()
        monster_loc = findimg(target_monster)
        # press 'q' to exit
    print('发现妖气!')
    enter_result = enter_yaoqi_party(monster_loc)
    if not enter_result:
        return find_monster(target_monster, refresh_location)
    else:
        return True



