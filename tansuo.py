import constants
import time
from findimg import *
import img
from utilities import *
from ctypes import windll
import utilities
from PIL import Image, ImageEnhance
from grabscreen import grab_screen
import pytesseract
import logging
import combat
import random
import pyautogui
import re
import enum
from concurrent.futures import ThreadPoolExecutor, as_completed


user32 = windll.user32
user32.SetProcessDPIAware()
constants.init_constants()
logging.basicConfig(
    level=0,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
_CAPTAINSLOT = 3



def color_code_convert(color_str, original_scale=(2048, 1536), current_res=get_window_info()[2:]):
    base, offset, accuracy, x_start, y_start, x_end, y_end = color_str[1:-1].split(', ')
    new_x0, new_y0 = cordinates_convert((float(x_start), float(y_start)), constants.WINDOW_ATTRIBUTES)
    new_x1, new_y1 = cordinates_convert((float(x_end), float(y_end)), constants.WINDOW_ATTRIBUTES)
    color_list = [[(0, 0), hex2rgb(base[2:])]]
    for i in offset[1:-1].split(','):
        offset_x, offset_y, color = i.split('|')
        offset_x = int(float(offset_x) / original_scale[0] * current_res[0])
        offset_y = int(float(offset_y) / original_scale[1] * current_res[1])
        color = hex2rgb(color[2:])
        color_list.append([(offset_x, offset_y), color])
    return f"ColorToMatch(({new_x0}, {new_y0}, {new_x1}, {new_y1}), {color_list}, {100-int(accuracy)})"


color_str = '{0xf8f9ff, "18|16|0x343b6b,-19|14|0xe2e4fc,4|40|0x3e2215,-4|-44|0xf1acb6", 95, 0, 0, 1535, 2047}'

color_code_convert(color_str)


def change_ss(ss_num):
    if ss_num in (1, 2, 3):
        click(1050, 1067)
    else:
        click(289, 726)

normalize_color_list([[(556, 521), (138, 27, 27)],
                      [(550, 500), (40, 99, 119)],
                      [(570, 500), (193, 168, 132)]])

raw_exp_full = [[(1015, 541), (252, 156, 26)], [(1012, 550), (234, 174, 17)],[(1036, 559), (249, 221, 6)]]
raw_in_dugeon = [(61, 808), (153, 53, 91)],[(53, 911),(97, 90, 118)],[(215, 972), (58, 44, 87)]
raw_loot = [[(991, 486), (178, 68, 30)], [(977, 475), (255, 244, 212)], [(1011, 500), (255, 244, 212)]]
raw_enter_dungeon = [[(1205, 750), (243, 178, 94)], [(1332, 782),(243, 178, 94)], [(825, 762), (243, 178, 94)]]
class TansuoColor:
    EnterDungeon = ColorToMatch((1200, 720, 1250, 780), normalize_color_list(raw_enter_dungeon), 2)
    InDungeon = ColorToMatch((40,780,80, 820), normalize_color_list(raw_in_dugeon), 1)
    ExpIcon = ColorToMatch((97, 323, 1646, 830),
                           [[(0, 0), (138, 27, 27)], [(-6, -21), (40, 99, 119)], [(14, -21), (193, 168, 132)]], 5)
    CombatIcon = ColorToMatch((0, 0, 1727, 1018),
                              [[(0, 0), (229, 230, 248)], [(-14, 31), (237, 163, 172)], [(-23, -13), (66, 77, 132)]], 10)
    CombatBoss = ColorToMatch((0, 0, 1727, 1018),
                              [[(0, 0), (239, 178, 186)], [(1, 57), (226, 206, 194)], [(-14, 85), (234, 165, 172)],
                               [(25, 63), (65, 37, 23)]], 10)
    BossLoot = ColorToMatch((552, 255, 1126, 809), normalize_color_list(raw_loot), 1)



TansuoExpColor = {
    1: ColorToMatch((849, 424, 1208, 837), normalize_color_list(raw_exp_full), 15),
    2: ColorToMatch((584, 306, 796, 630), normalize_color_list(raw_exp_full), 15),
    3: ColorToMatch((296, 283, 556, 545), normalize_color_list(raw_exp_full), 15),
}

slot_loc = {1:[277, 526],
            2:[853, 520],
            3:[1436, 514]}

mons_loc = [[648, 831], [808, 820], [978, 827]]


class TansuoResult(enum.Enum):
    FinishedWithBoss = 0
    FinishedWithoutBoss =1


def detect_full_exp_mons():
    global _CAPTAINSLOT
    need_change_table = []
    for k, v in TansuoExpColor.items():
        if k != _CAPTAINSLOT:
            if myFindColor(v):
                logging.info(f'{k} 号位狗粮已经满级!')
                need_change_table.append(k)
    return need_change_table



def swap_full_exp_mons():
    wait_for_color(CombatColor.Ready)
    need_change_mons = detect_full_exp_mons()
    if need_change_mons:
        click((100, 743), tired_check=True, random_range=5)
        logging.debug('更换狗粮中。。。')
        utilities.random_sleep(2, 1)
        click((113, 928), tired_check=False, random_range=5)
        utilities.random_sleep(0.2, 0.2)
        click((228, 525), tired_check=False, random_range=5)

    utilities.random_sleep(0.5, 0.5)
    for num, change in enumerate(need_change_mons):
        this_mons_loc_x = mons_loc[num][0] + random.randrange(-10, 10)
        this_mons_loc_y = mons_loc[num][1] + random.randrange(-10, 10)
        constants.INPUT_CONTROLLER.move(x=this_mons_loc_x, y=this_mons_loc_y, duration=0.2)
        constants.INPUT_CONTROLLER.click_down()
        constants.INPUT_CONTROLLER.move(x=this_mons_loc_x,
                                        y=this_mons_loc_y-240-random.randrange(20),
                                        duration=0.2)
        constants.INPUT_CONTROLLER.move(x=slot_loc[change][0]+random.randrange(-10, 10),
                                        y=slot_loc[change][1]++random.randrange(-10, 10),
                                        duration=0.2)
        constants.INPUT_CONTROLLER.click_up()
        utilities.random_sleep(0.5, 0.5)



def tansuo_to_dungeon():
    enter_dugeon_loc = wait_for_color(TansuoColor.EnterDungeon, max_time=5)
    if enter_dugeon_loc:
        click(enter_dugeon_loc)
        in_dugeon = wait_for_color(TansuoColor.InDungeon)
        if not in_dugeon:
            return tansuo_to_dungeon()
    else:
        constants.INPUT_CONTROLLER.move(1564+random.randrange(-50, 50), 648+random.randrange(-50, 50))
        time.sleep(0.2)
        for i in range(random.randrange(50, 100)):
            constants.INPUT_CONTROLLER.scroll()
            time.sleep(0.01)
        click((1555, 870), random_range=15)
        return tansuo_to_dungeon()


def findexp_parallel(color, delay_gap=0.2, threads=5):
    delay_times = [delay_gap*(i+1) for i in range(threads)]
    colors = [color]*threads
    result_loc = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for out in as_completed([executor.submit(delay_find_color, *vars)
                                 for vars in zip(colors, delay_times)]):
            result_loc.append(out.result())
    valid_results = [i for i in result_loc if i]
    if valid_results:
        return valid_results[0]
    else:
        return None


def search_for_exp(fight_count):
    count = 0
    print('寻找经验怪, 同屏找怪5秒')
    search_t = datetime.datetime.now()
    while (datetime.datetime.now() - search_t).total_seconds() <= 5:
        # print(f'找怪第{count}次')
        exp_loc = myFindColor(TansuoColor.ExpIcon)
        if exp_loc:
            print('找到经验怪')
            # click(exp_loc)
            accept_invite()
            combat_loc = myFindColor(
                ColorToMatch((max(exp_loc[0] - 200, 0), max(exp_loc[1] - 500,0), exp_loc[0] + 200, exp_loc[1] - 30),
                             [[(0, 0), (229, 230, 248)], [(-14, 31), (237, 163, 172)], [(-23, -13), (66, 77, 132)]], 10))
            if combat_loc:
                print('找到战斗')
                click(combat_loc)
                time.sleep(0.5)
                # if_outof_sushi()
                combat_loc = myFindColor(TansuoColor.CombatIcon)
                if combat_loc:
                    print('进入战斗失败')
                    # check_current_state()
                    return search_for_exp(fight_count)

                swap_full_exp_mons()
                this_fight = combat.Combat('探索', combat_time_limit=60 * 1 + random.randint(40, 80))
                combat_result = this_fight.start(auto_ready=False)
                time.sleep(1)
                wait_for_color(TansuoColor.InDungeon)
                boss_loc = myFindColor(TansuoColor.CombatBoss)
                if boss_loc:
                    click(boss_loc)
                    fight_count = fight_count + 1
                    this_fight = combat.Combat('探索BOSS', combat_time_limit=60 * 1 + random.randint(40, 80))
                    combat_result = this_fight.start(auto_ready=False)
                    time.sleep(2)
                    loc = wait_for_color(TansuoColor.InDungeon)
                    if loc:
                        logging.info('loot found!')
                        loot_loc = myFindColor(TansuoColor.BossLoot)
                        while loot_loc:
                            click(loot_loc, tired_check=True)
                            utilities.random_sleep(0.5, 1)
                            click((90, 943), tired_check=True, random_range=10)
                            utilities.random_sleep(1.5, 1)
                            loot_loc = myFindColor(TansuoColor.BossLoot)
                    return TansuoResult.FinishedWithBoss
                return search_for_exp(fight_count)
            else:
                print('未找到战斗')
                return search_for_exp(fight_count)
        else:
            print('未找到经验怪')
        count = count + 1

def next_scene():
    print('滑动进下一界面')
    constants.INPUT_CONTROLLER.move(1680, 787)
    constants.INPUT_CONTROLLER.drag(x0=1686, y0=787, x1=687, y1=787, duration=0.2)


def one_tansuo():
    wait_for_color(TansuoColor.InDungeon)
    fight_count = 0
    search_for_exp(fight_count)
    for find_time in range(4):
        print(f'找怪第{find_time+1}次')
        next_scene()
        search_for_exp(fight_count)
        result = wait_for_color(TansuoColor.InDungeon)
        if result == TansuoResult.FinishedWithBoss:
            return result
    click((77, 124), random_range=3)
    utilities.random_sleep(0.5, 1)
    click((1030, 557), random_range=3, tired_check=False)
    wait_for_color(TansuoColor.EnterDungeon)
    return TansuoResult.FinishedWithoutBoss



def repeat_tansuo(times=10):
    t = 0
    while t < times:
        tansuo_to_dungeon()
        result = one_tansuo()


if __name__ == '__main__':
    repeat_tansuo(15)


