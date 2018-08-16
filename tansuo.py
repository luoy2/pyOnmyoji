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

user32 = windll.user32
user32.SetProcessDPIAware()
constants.init_constants()
logging.basicConfig(
    level=0,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")


def cordinates_convert(cords, original_scale=(2048, 1536), current_res=get_window_info()[2:]):
    new_x = round(cords[0] / original_scale[0] * current_res[0])
    new_y = round(cords[1] / original_scale[1] * current_res[1])
    return (new_x, new_y)


def color_code_convert(color_str, original_scale=(2048, 1536), current_res=get_window_info()[2:]):
    base, offset, accuracy, x_start, y_start, x_end, y_end = color_str[1:-1].split(', ')
    new_x0, new_y0 = cordinates_convert((float(x_start), float(y_start)))
    new_x1, new_y1 = cordinates_convert((float(x_end), float(y_end)))
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
        click(cordinates_convert((1050, 1067)))
    else:
        click(cordinates_convert((289, 726)))



normalize_color_list([[(556, 521), (138, 27, 27)],
                      [(550, 500), (40, 99, 119)],
                      [(570, 500), (193, 168, 132)]])

class TansuoColor:
    ExpIcon = ColorToMatch((0, 0, 1727, 1018),
                           [[(0, 0), (138, 27, 27)], [(-6, -21), (40, 99, 119)], [(14, -21), (193, 168, 132)]], 5)
    CombatIcon = ColorToMatch((0, 0, 1727, 1018),
                              [[(0, 0), (229, 230, 248)], [(-14, 31), (237, 163, 172)], [(-23, -13), (66, 77, 132)]], 10)
    CombatBoss = ColorToMatch((0, 0, 1727, 1018), [[(0, 0), (239, 178, 186)], [(1, 57), (226, 206, 194)], [(-14, 85), (234, 165, 172)], [(25, 63), (65, 37, 23)]], 10)

def search_for_exp(fight_count):
    count = 0
    print('寻找经验怪, 同屏找怪3秒')
    search_t = datetime.datetime.now()
    while (datetime.datetime.now() - search_t).total_seconds() <= 3:
        accept_invite()
        exp_loc = myFindColor(TansuoColor.ExpIcon)
        if exp_loc:
            print('找到经验怪')
            # click(exp_loc)
            accept_invite()
            combat_loc = myFindColor(
                ColorToMatch((exp_loc[0] - 200, exp_loc[1] - 500, exp_loc[0] + 200, exp_loc[1] - 30),
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
                # if if_start_combat_intime() then
                # else
                #   print('战斗未开始, 跳出战斗循环')
                #   return search_for_exp(fight_count)
                #
                # print('检测狗粮')
                # accept_invite()
                # local ready_x, ready_y = findMultiColorInRegionFuzzy(0xfffffa,"5|-39|0xfffff9,27|-34|0xfff3d1,
                # 27|-1|0xfffaeb,51|-17|0xfff2d0", 90, 1789, 1274, 1798, 1283)
                # wait_for_state(准备)
                # if_change(slot, tonumber(_G.skiplines))
                this_fight = combat.Combat('探索', combat_time_limit=60 * 1 + random.randint(40, 80))
                combat_result = this_fight.start(auto_ready=False)
                time.sleep(1)
                # wait_for_state(副本里面)
                boss_loc = myFindColor(TansuoColor.CombatBoss)
                if boss_loc:
                    click(boss_loc)
                    fight_count = fight_count + 1
                    this_fight = combat.Combat('探索BOSS', combat_time_limit=60 * 1 + random.randint(40, 80))
                    combat_result = this_fight.start(auto_ready=False)
                return search_for_exp(fight_count)
            else:
                print('未找到战斗')
                return search_for_exp(fight_count)
        else:
            print('未找到经验怪')
        count = count + 1

def next_scene():
    print('滑动进下一界面')
        # if _G.target_chapter == 11 then
        # 	my_swip(1977, 1346, 1300, 1346, 35)
        # else
    constants.INPUT_CONTROLLER.move(1680, 787)
    constants.INPUT_CONTROLLER.drag(x0=1686, y0=787, x1=687, y1=787, duration=0.2)
	# end
# end


fight_count = 0
search_for_exp(fight_count)
for find_time in range(4):
    print(f'找怪第{find_time+1}次')
    next_scene()
    search_for_exp(fight_count)



