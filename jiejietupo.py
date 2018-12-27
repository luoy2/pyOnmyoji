import constants
import time
from findimg import *
import img
from ctypes import windll
import utilities
from PIL import Image, ImageEnhance
from grabscreen import grab_screen
import pytesseract
import logging
import combat
import random
import pyautogui
import sys


class LiaotupoFinishedException(Exception):
    pass

class EnterJiejieDashboardFailed(Exception):
    pass


def enter_tupo():
    click((429, 940), tired_check=True, need_convert=True)
    utilities.random_sleep(1, 1.5)


class MainJiejie:

    def __init__(self, retry_time=10):
        self.retry_time = retry_time

    def tap_to_main(self):
        count = 0
        while not myFindColor(LocatorColor.Jiejie):
            # print(pyautogui.pixel(self.x, self.y))
            utilities.random_sleep(0.1, 0.2)
            click((491, 113), random_range=20, tired_check=False, need_convert=True)
            count += 1
            if count > self.retry_time:
                logging.info(f'failed to enter jiejie for {self.retry_time}.')
                raise EnterJiejieDashboardFailed


class JIEJIE_OCR_LOCATION:
    PERSONAL_TUPO_CHANCE_LEFT = (554, 860, 590, 888)
    LIAOTUPO_CHANCE_LEFT = (360, 840, 390, 885)
    PERSONAL_WAITING_MINUTE = (1403, 751, 1446, 788)
    PERSONAL_WAITING_SECOND = (1460, 751, 1503, 787)



class FinishedJiejie:
    x_offset = 1502-1097 #405
    y_offset = 249-167 #82
    color = (95, 22, 35)


class FailedJiejie:
    x_offset = 1060-640 #414
    y_offset = 1271-1225 #12
    color = (225, 188, 98)



class Metals:
    y_offset =291-167 # 124
    x_offset_list = [163+53*i for i in range(5)]
    color = (179, 162, 141)
    finished_color = (89, 81, 70)



class LiaoTupoTargetsCords(list):
    def __init__(self):
        super().__init__()
        x_start = 555
        y_start = 186
        x_end = 1003
        y_end = 363

        y_add = 180
        x_add = 1006 - 555
        x_add, y_add = cordinates_scale((x_add, y_add), constants.WINDOW_ATTRIBUTES)

        x1, y1 = cordinates_convert((x_start, y_start), constants.WINDOW_ATTRIBUTES)
        x2, y2 = cordinates_convert((x_end, y_end), constants.WINDOW_ATTRIBUTES)
        start_loc = [x1, y1, x2, y2]
        for row in range(4):
            for col in range(2):
                cords = [start_loc[0] + x_add*col,
                        start_loc[1] + y_add*row,
                        start_loc[2] + x_add*col,
                        start_loc[3] + y_add*row]
                self.append(cords)


class PersonalTupoTargetsCords(list):
    def __init__(self):
        super().__init__()
        x_start = 183
        y_start = 167
        x_end = 631
        y_end = 344

        y_add = 348 - 167
        x_add = 640 - 183
        x_add, y_add = cordinates_scale((x_add, y_add), constants.WINDOW_ATTRIBUTES)

        x1, y1 = cordinates_convert((x_start, y_start), constants.WINDOW_ATTRIBUTES)
        x2, y2 = cordinates_convert((x_end, y_end), constants.WINDOW_ATTRIBUTES)
        start_loc = [x1, y1, x2, y2]
        # Image.fromarray(grab_screen(start_loc)).show()
        for row in range(3):
            for col in range(3):
                cords = [start_loc[0] + x_add*col,
                        start_loc[1] + y_add*row,
                        start_loc[2] + x_add*col,
                        start_loc[3] + y_add*row]
                self.append(cords)


class LiaoTuPo:
    def __init__(self):
        self.logger = logging.getLogger('Liao Tupo Dashboard')
        self.targets_cords = LiaoTupoTargetsCords()
        self.current_page = 0
        self.avaliable_target_page = 0

    def enter_liaotupo(self):
        wait_for_state(img.jiejietupo_img.MAIN_TUPO)


    def next_page(self):
        for i in range(4):
            pyautogui.moveTo(cordinates_convert((1097, 512), constants.WINDOW_ATTRIBUTES))
            constants.INPUT_CONTROLLER.scroll()
            time.sleep(0.2)
            constants.INPUT_CONTROLLER.scroll()
            time.sleep(0.2)


    def get_remain_chance(self):
        accept_invite()
        x1, y1 = cordinates_convert((381, 777), constants.WINDOW_ATTRIBUTES)
        x2, y2 = cordinates_convert((400, 804), constants.WINDOW_ATTRIBUTES)
        img = grab_screen([x1, y1, x2, y2])
        img = Image.fromarray(img)
        remain = int(pytesseract.image_to_string(img, config='-psm 6').replace('O', '0'))
        self.logger.debug(f'remaining chance: {remain}')
        return remain


    def get_next_avaliable_target(self):
        self.logger.info(f'move to page {self.avaliable_target_page}')
        # for i in range(self.avaliable_target_page-self.current_page):
        #     self.next_page()
        #     self.current_page+=1
        single_target = None
        for i in self.targets_cords:
            single_target = SingleTarget(i)
            if single_target.avaliable:
                break
            if single_target.finished:
                self.logger.info('所有结界都已经被突破！')
                raise LiaotupoFinishedException
        if not single_target.avaliable:
            self.logger.info('cannot find avaliable target in this page!')
            # self.avaliable_target_page += 1
            self.next_page()
            return self.get_next_avaliable_target()
        return single_target


class PersonalTuPo:

    def __init__(self, desc=True):
        import constants
        self.waiting_color = (176, 169, 161)
        self.waiting_color_cords = cordinates_convert((1402, 771), constants.WINDOW_ATTRIBUTES)
        self.logger = logging.getLogger(u'个人突破main')
        self.targets_cords = PersonalTupoTargetsCords()
        self.desc=desc

    def enter_pensonaltupo(self):
        wait_for_state(img.jiejietupo_img.MAIN_TUPO)


    def wait_for_next_refresh(self):
        while pyautogui.pixelMatchesColor(self.waiting_color_cords[0],
                                          self.waiting_color_cords[1],
                                          self.waiting_color):
            accept_invite()
            MINUTE_CORDS = add_pos_with_offset(JIEJIE_OCR_LOCATION.PERSONAL_WAITING_MINUTE, constants.WINDOW_ATTRIBUTES)
            SECOND_CORDS = add_pos_with_offset(JIEJIE_OCR_LOCATION.PERSONAL_WAITING_SECOND, constants.WINDOW_ATTRIBUTES)
            minute_img = Image.fromarray(grab_screen(MINUTE_CORDS))
            minute_str = pytesseract.image_to_string(minute_img, lang='eng', config='-psm 6').replace('O', '0')
            second_img = Image.fromarray(grab_screen(SECOND_CORDS))
            second_str = pytesseract.image_to_string(second_img, lang='eng', config='-psm 6').replace('O', '0')
            try:
                waiting_second = int(minute_str) * 60 + int(second_str)
                logging.info(f'waiting time: {minute_str}:{second_str}...')
                return time.sleep(waiting_second)
            except Exception as e:
                logging.debug(f'minute_str: {minute_str}; second_str: {second_str}')
                time.sleep(1)


    def refresh(self):
        self.wait_for_next_refresh()
        click((1404, 772), need_convert=True)
        utilities.random_sleep(1, 1)
        click((1040, 633), need_convert=True)



    def get_remain_chance(self):
        chance_location = add_pos_with_offset(JIEJIE_OCR_LOCATION.PERSONAL_TUPO_CHANCE_LEFT, constants.WINDOW_ATTRIBUTES)
        img = grab_screen(chance_location)
        img = Image.fromarray(img)
        remain = int(pytesseract.image_to_string(img, config='-psm 6').replace('O', '0'))
        self.logger.debug(f'remaining chance: {remain}')
        return remain



    def get_tupo_page_status(self):
        win_count = 0
        avaliable_targets = []
        for i in self.targets_cords:
            single_target = SingleTarget(i)
            if single_target.finished:
                win_count+=1
            elif single_target.avaliable:
                avaliable_targets.append(single_target)
        avaliable_targets.sort(key=lambda x: x.metals, reverse=self.desc)
        return win_count, avaliable_targets


class SingleTarget:
    avaliable = None
    metals = 0
    #TODO check metal number
    def __init__(self, region):
        self.region = region
        self.logger = logging.getLogger('Single Tupo Target')
        # self.name = self.get_name()
        self.avaliable = self._check_avaliablilty()
        self._check_metal()
        if self.avaliable:
            self.logger.debug(f'tupo target at {self.region} avaliable.')
        # self.metals = self._check_metal()

    def _check_not_failed(self):
        fail_x, fail_y = cordinates_scale((FailedJiejie.x_offset, FailedJiejie.y_offset), constants.WINDOW_ATTRIBUTES)
        fail_x = self.region[0] + fail_x
        fail_y = self.region[1] + fail_y
        self.failed = pyautogui.pixelMatchesColor(fail_x, fail_y, FailedJiejie.color, tolerance=10)
        if self.failed:
            self.logger.debug(f'tupo target at {self.region} failed.')
            return 0
        return 1

    def _check_not_finished(self):
        finished_x, finished_y = cordinates_scale((FinishedJiejie.x_offset, FinishedJiejie.y_offset), constants.WINDOW_ATTRIBUTES)
        finished_x = self.region[0] + finished_x
        finished_y = self.region[1] + finished_y
        self.finished = pyautogui.pixelMatchesColor(finished_x, finished_y, FinishedJiejie.color, tolerance=15)
        if self.finished:
            self.logger.debug(f'tupo target at {self.region} finished.')
            return 0
        return 1

    # TODO: Check metal number
    def _check_metal(self):
        metals = Metals()
        total_metal = 0
        for x_offset in metals.x_offset_list:
            x, y = cordinates_scale((x_offset, metals.y_offset), constants.WINDOW_ATTRIBUTES)
            metal_x = x + self.region[0]
            metal_y = y + self.region[1]
            if not self.finished:
                if not pyautogui.pixelMatchesColor(metal_x, metal_y, Metals.color, tolerance=10):
                    total_metal += 1
            else:
                if not pyautogui.pixelMatchesColor(metal_x, metal_y, Metals.finished_color, tolerance=2):
                    total_metal += 1
            # print(metal_x, metal_y)
        self.metals = total_metal
        self.logger.debug(f'total metals: {total_metal}')



    def _check_avaliablilty(self):
        not_fail = self._check_not_failed()
        not_finish = self._check_not_finished()
        return not_finish and not_fail





def main_liaotupo():
    '''
    1. 锁定阵容
    2，进入寮突破
    3. 开始挂机
    :return:
    '''
    tupo_main = MainJiejie()
    tupo_main.tap_to_main()
    liao_tupo = LiaoTuPo()
    remain = liao_tupo.get_remain_chance()

    while remain:
        try:
            next_target = liao_tupo.get_next_avaliable_target()
            click((int((next_target.region[2] + next_target.region[0])/2),
                   int((next_target.region[3] + next_target.region[1])/2)))
            this_color = JiejieColor.LiaoAttack
            y_offset_top, y_offset_bottom = 593-729, 920-549
            y_offset_top, y_offset_bottom = cordinates_scale((y_offset_top, y_offset_bottom), constants.WINDOW_ATTRIBUTES)
            this_color.region = [next_target.region[0], next_target.region[1]+y_offset_top,
                                 next_target.region[2], next_target.region[1]+y_offset_bottom]
            this_color.screen_shot_region = this_color.get_region_to_screenshot()
            time.sleep(1)
            attack_cords = wait_for_color(this_color)
            accept_invite()
            click(attack_cords)
            this_fight = combat.Combat('阴阳寮突破', combat_time_limit=60*5+random.randint(40, 80))
            try:
                combat_result = this_fight.start(auto_ready=True)
            except TimeoutError:
                logging.warning('Failed to finish tupo combat!')
                accept_invite()
                click((986, 629), tired_check=False, need_convert=True)
                escape()
                utilities.random_sleep(1, 0.5)
                accept_invite()
                click((986, 629), tired_check=False, need_convert=True)
                combat_result = this_fight.start(auto_ready=True)
            tupo_main.tap_to_main()
            liao_tupo.current_page = 0
            logging.debug('finished one tupo')
            remain = liao_tupo.get_remain_chance()
        except LiaotupoFinishedException:
            # no need to continue
            return 0
    return 1

def main_personaltupo(refresh_time=3, desc=True):
    '''
    1. 锁定阵容
    2，进入寮突破
    3. 开始挂机
    :return:
    '''
    tupo_main = MainJiejie()
    tupo_main.tap_to_main()
    personal_tupo = PersonalTuPo(desc)
    remain = personal_tupo.get_remain_chance()

    while remain:
        win_count, avaliable_targets = personal_tupo.get_tupo_page_status()
        if win_count < refresh_time:
            next_target = avaliable_targets[0]
            logging.debug(f'this target have {next_target.metals} metal.')
            click((int((next_target.region[2] + next_target.region[0])/2),
                   int((next_target.region[3] + next_target.region[1])/2)))
            this_color = JiejieColor.PersonalAttack
            x_offset, y_offset = 423-185, 547-171
            x_offset, y_offset = cordinates_scale((x_offset, y_offset), constants.WINDOW_ATTRIBUTES)
            this_color.region = [next_target.region[0], next_target.region[1],
                                 next_target.region[2]+x_offset, next_target.region[1]+y_offset]
            this_color.screen_shot_region = this_color.get_region_to_screenshot()
            time.sleep(1)
            attack_cords = wait_for_color(this_color)
            accept_invite()
            click(attack_cords)
            this_fight = combat.Combat('结界突破', combat_time_limit=60*2+random.randint(40, 80))
            try:
                combat_result = this_fight.start(auto_ready=True)
            except TimeoutError:
                logging.warning('Failed to finish tupo combat!')
                accept_invite()
                click((986, 629), tired_check=False, need_convert=True)
                escape()
                utilities.random_sleep(1, 0.5)
                accept_invite()
                click((986, 629), tired_check=False, need_convert=True)
                combat_result = this_fight.start(auto_ready=True)
            logging.debug('finished one tupo')
            tupo_main.tap_to_main()
            remain = personal_tupo.get_remain_chance()
        else:
            personal_tupo.refresh()
            wait_for_state(img.jiejietupo_img.MAIN_TUPO)
    return 0


def main_all_tupo(refrehs_time=3, desc=True):
    accept_invite()
    liao_status = main_liaotupo()
    click((1648, 333), need_convert=True)
    personal_status = main_personaltupo(refrehs_time, desc)
    click((1648,505), need_convert=True)
    while personal_status or liao_status:
        liao_status = main_liaotupo()
        escape()
        time.sleep((10+random.randrange(10, 20))*60)
        wait_for_color(LocatorColor.Main)
        time.sleep(1)
        constants.INPUT_CONTROLLER.move(1570, 720)
        constants.INPUT_CONTROLLER.drag(x0=1570+random.randrange(30),
                                        y0=720-random.randrange(10),
                                        x1=173+random.randrange(30), y1=720-random.randrange(10), duration=0.5)
        utilities.random_sleep(0.2, 0.5)
        click((681, 263), random_range=10, need_convert=True)
        wait_for_color(LocatorColor.Map)
        click((420, 943), random_range=3, need_convert=True)
        utilities.random_sleep(1, 2)
        click((1648, 505), random_range=3, need_convert=True)
        utilities.random_sleep(1, 1.5)



if __name__ == '__main__':
    user32 = windll.user32
    user32.SetProcessDPIAware()

    constants.init_constants(u'阴阳师-网易游戏', move_window=1)
    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")
    main_all_tupo(3, True)



# x = PersonalTuPo()
# x.wait_for_next_refresh()


# main_liaotupo()
# for i in targets_cords:
#     single_target = SingleTarget(i)
#     # o = grab_screen(single_target.region)
#     # o = Image.fromarray(o)
#     # o.show()
#
#
# o = grab_screen([640, 167, 1088, 344])
# o = Image.fromarray(o)
# o.show()

# #
# o = grab_screen((633, 134, 1600, 987))
# o = Image.fromarray(o)
# o.show()
# pyautogui.locateCenterOnScreen('res/jiejietupo/attack.png',region=(633, 134, 1600, 987),confidence=0.9,grayscale=False)
#
#

# img = grab_screen(constants.WINDOW_OFFSET)
# img = grab_screen((774, 232, 933, 276))
# img = Image.fromarray(img)
# img.show()
# pytesseract.image_to_string(img, lang='chi_sim')
# pytesseract.image_to_string(img, config='-psm 6')

#     print(cords)
#     img = grab_screen(cords)
#     img = Image.fromarray(img)
#     # enhancer = ImageEnhance.Contrast(img)
#     # img = enhancer.enhance(2)
#     # img = img.convert('1')
#     img.show()
#
#
# target_loc_list.append(row_list)

