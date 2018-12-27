from findimg import *
from colors import *
from ctypes import windll
import utilities
import combat
import enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from controller import *
from jiejietupo import *





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




def change_ss(ss_num):
    if ss_num in (1, 2, 3):
        click((1050, 1067), need_convert=True)
    else:
        click((289, 726), need_convert=True)




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
        accept_invite()
        utilities.random_sleep(2, 1)
        click((100, 743), tired_check=True, random_range=1)
        click((100, 743), tired_check=True, random_range=1)
        logging.debug('更换狗粮中。。。')
        utilities.random_sleep(2, 1)
        accept_invite()
        click((113, 928), tired_check=False, random_range=1)
        utilities.random_sleep(0.2, 0.2)
        accept_invite()
        click((228, 525), tired_check=False, random_range=1)

    utilities.random_sleep(0.5, 0.5)
    for num, change in enumerate(need_change_mons):
        this_mons_loc_x = mons_loc[num][0] + random.randrange(-10, 10)
        this_mons_loc_y = mons_loc[num][1] + random.randrange(-10, 10)
        constants.INPUT_CONTROLLER.move(x=this_mons_loc_x, y=this_mons_loc_y, duration=0.2)
        accept_invite()
        constants.INPUT_CONTROLLER.click_down()
        accept_invite()
        constants.INPUT_CONTROLLER.move(x=this_mons_loc_x,
                                        y=this_mons_loc_y-240-random.randrange(20),
                                        duration=0.2)
        accept_invite()
        constants.INPUT_CONTROLLER.move(x=slot_loc[change][0]+random.randrange(-10, 10),
                                        y=slot_loc[change][1]++random.randrange(-10, 10),
                                        duration=0.2)
        constants.INPUT_CONTROLLER.click_up()
        utilities.random_sleep(0.5, 0.5)



def tansuo_to_dungeon():
    logging.info('尝试进入副本。')
    enter_dugeon_loc = wait_for_color(TansuoColor.EnterDungeon, max_time=5)
    if enter_dugeon_loc:
        click(enter_dugeon_loc)
        in_dugeon = wait_for_color(TansuoColor.InDungeon)
        if not in_dugeon:
            return tansuo_to_dungeon()
    else:
        loc = map_locator()
        if loc == LocatorColor.Main:
            time.sleep(1)
            constants.INPUT_CONTROLLER.move(1570, 720)
            constants.INPUT_CONTROLLER.drag(x0=1570 + random.randrange(30),
                                            y0=720 - random.randrange(10),
                                            x1=173 + random.randrange(30), y1=720 - random.randrange(10),
                                            duration=0.5)
            utilities.random_sleep(0.2, 0.5)
            click((681, 263), random_range=10, need_convert=True)
            wait_for_color(LocatorColor.Map)
        elif loc == LocatorColor.Map:
            pass
        else:
            raise KeyError
        constants.INPUT_CONTROLLER.move(1564+random.randrange(-50, 50), 648+random.randrange(-50, 50))
        time.sleep(0.2)
        for i in range(random.randrange(50, 100)):
            constants.INPUT_CONTROLLER.scroll()
            time.sleep(0.01)
        click((1555, 870), random_range=15, need_convert=True)
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
                logging.debug('找到战斗')
                click(combat_loc, tired_check=False)
                time.sleep(1)
                if_outof_sushi()
                combat_loc = myFindColor(TansuoColor.CombatIcon)
                if combat_loc:
                    logging.debug('进入战斗失败')
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
                    time.sleep(3)
                    loc = wait_for_color(TansuoColor.InDungeon, max_time=5)
                    if loc:
                        logging.info('loot found!')
                        loot_loc = myFindColor(TansuoColor.BossLoot)
                        while loot_loc:
                            logging.info('picking up loot')
                            accept_invite()
                            click(loot_loc, tired_check=True)
                            utilities.random_sleep(0.5, 1)
                            accept_invite()
                            click((90, 943), tired_check=True, random_range=10, need_convert=True)
                            utilities.random_sleep(1.5, 1)
                            loot_loc = myFindColor(TansuoColor.BossLoot)
                    else:
                        logging.info('no loot, enter dungeon')
                    print('完成boss战斗')
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
    constants.INPUT_CONTROLLER.drag(x0=1680, y0=787, x1=687, y1=787, duration=0.2)


import win32com.client
def one_tansuo():
    wait_for_color(TansuoColor.InDungeon)
    fight_count = 0
    search_for_exp(fight_count)
    for find_time in range(4):
        print(f'找怪第{find_time+1}次')
        next_scene()
        result = search_for_exp(fight_count)
        if result == TansuoResult.FinishedWithBoss:
            print('finished with boss')
            # while 1:
            #     result = find_color(ChaoGuiColor.FindChaoGui)
            #     if result:
            #         pyautogui.click((510, 392))
            #         speaker = win32com.client.Dispatch("SAPI.SpVoice")
            #         speaker.Speak(u"Found Guiwang")
            #         pyautogui.click((510, 392))
            #         time.sleep(99999)
            #     time.sleep(0.1)
            return result
        wait_for_color(TansuoColor.InDungeon)
    accept_invite()
    click((77, 124), random_range=3, need_convert=True)
    utilities.random_sleep(0.5, 1)
    accept_invite()
    click((1030, 557), random_range=3, tired_check=False, need_convert=True)
    wait_for_color(TansuoColor.EnterDungeon)
    return TansuoResult.FinishedWithoutBoss



def repeat_tansuo(times=999, liao_sep=8, liao_status=1):
    t = 0
    while t < times:
        tansuo_to_dungeon()
        result = one_tansuo()
        t += 1
        if not t%liao_sep:
            escape()
            loc = map_locator()
            if loc == LocatorColor.Main:
                time.sleep(1)
                constants.INPUT_CONTROLLER.move(1570, 720)
                constants.INPUT_CONTROLLER.drag(x0=1570 + random.randrange(30),
                                                y0=720 - random.randrange(10),
                                                x1=173 + random.randrange(30), y1=720 - random.randrange(10),
                                                duration=0.5)
                utilities.random_sleep(0.2, 0.5)
                accept_invite()
                click((681, 263), random_range=10, need_convert=True)
                wait_for_color(LocatorColor.Map)
            elif loc == LocatorColor.Map:
                pass
            else:
                raise KeyError
            time.sleep(2)
            enter_tupo()
            if liao_status:
                accept_invite()
                click((1648, 505), random_range=3, need_convert=True)
                liao_status = main_liaotupo()
                accept_invite()
                click((1648, 333), need_convert=True)
            personal_status = main_personaltupo()
            if liao_status:
                accept_invite()
                click((1648,505), need_convert=True)
                liao_status = main_liaotupo()
            escape()



if __name__ == '__main__':
    liao_status = 1
    # personal_status = 0
    user32 = windll.user32
    user32.SetProcessDPIAware()
    constants.init_constants(move_window=1)
    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    _CAPTAINSLOT = 3
    enter_tupo()
    if liao_status:
        accept_invite()
        click((1648, 505), random_range=3, need_convert=True)
        liao_status = main_liaotupo()
        accept_invite()
        click((1648, 333), need_convert=True)
    personal_status = main_personaltupo()
    if liao_status:
        accept_invite()
        click((1648, 505), need_convert=True)
        liao_status = main_liaotupo()
    escape()
    time.sleep(3)
    loc = map_locator()
    if loc == LocatorColor.Main:
        time.sleep(1)
        constants.INPUT_CONTROLLER.move(1570, 720)
        constants.INPUT_CONTROLLER.drag(x0=1570 + random.randrange(30),
                                        y0=720 - random.randrange(10),
                                        x1=173 + random.randrange(30), y1=720 - random.randrange(10),
                                        duration=0.5)
        utilities.random_sleep(0.2, 0.5)
        accept_invite()
        click((681, 263), random_range=10, need_convert=True)
        wait_for_color(LocatorColor.Map)
    elif loc == LocatorColor.Map:
        pass
    else:
        raise KeyError
    repeat_tansuo(liao_status=liao_status)

