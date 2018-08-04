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

user32 = windll.user32
user32.SetProcessDPIAware()

import os
from multiprocessing import Process
constants.init_constants()
logging.basicConfig(
    level=0,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")

# time.sleep(2)
#

# constants.INPUT_CONTROLLER.click_string('6', game_frame=constants.WINDOW_OFFSET)
import enum
class JIEJIE_OCR_LOCATION:
    LIAOTUPO_LEFT = (360, 840, 390, 885)




class LiaoTuPo:
    def __init__(self):
        self.logger = logging.getLogger('Liao Tupo Dashboard')
        self.targets_cords = LiaoTupoTargetsCords()

    def enter_liaotupo(self):
        wait_for_state(img.jiejietupo_img.MAIN_TUPO)



    def next_page(self):
        pyautogui.moveTo(1097, 512)
        constants.INPUT_CONTROLLER.scroll()
        constants.INPUT_CONTROLLER.scroll()
        utilities.random_sleep()


    def get_remain_chance(self):
        x1 = JIEJIE_OCR_LOCATION.LIAOTUPO_LEFT[0] + constants.WINDOW_OFFSET[0]
        y1 = JIEJIE_OCR_LOCATION.LIAOTUPO_LEFT[1] + constants.WINDOW_OFFSET[1]
        x2 = JIEJIE_OCR_LOCATION.LIAOTUPO_LEFT[2] + constants.WINDOW_OFFSET[0]
        y2 = JIEJIE_OCR_LOCATION.LIAOTUPO_LEFT[3] + constants.WINDOW_OFFSET[1]
        img = grab_screen([x1, y1, x2, y2])
        img = Image.fromarray(img)
        remain = int(pytesseract.image_to_string(img, config='-psm 6'))
        self.logger.debug(f'remaining chance: {remain}')
        return remain


    def get_next_avaliable_target(self):
        single_target = None
        for i in self.targets_cords:
            single_target = SingleTarget(i)
            if single_target.avaliable:
                break
        if not single_target.avaliable:
            self.logger.info('cannot find avaliable target in this page!')
            for i in range(random.randint(1, 3)):
                self.next_page()
                time.sleep(0.5)
            return self.get_next_avaliable_target()
        return single_target


class SingleTarget:
    avaliable = None
    metals = 0
    #TODO check metal number
    def __init__(self, region):
        self.region = region
        self.logger = logging.getLogger('Single Tupo Target')
        # self.name = self.get_name()
        self.avaliable = self._check_avaliablilty()
        if self.avaliable:
            self.logger.debug(f'tupo target at {self.region} avaliable.')
        # self.metals = self._check_metal()


    def _check_not_failed(self):
        self.failed = findimg([img.jiejietupo_img.SINGLE_TARGET.FAILED, self.region], grayscale=False, confidence=0.9)
        if self.failed:
            self.logger.debug(f'tupo target at {self.region} failed.')
            return 0
        return 1

    def _check_not_finished(self):
        self.finished = findimg([img.jiejietupo_img.SINGLE_TARGET.FINISHED, self.region])
        if self.finished:
            self.logger.debug(f'tupo target at {self.region} finished.')
            return 0
        return 1


    def _check_metal(self):
        if self.finished:
            metals = findimg_all([img.jiejietupo_img.SINGLE_TARGET.FINISHED_METAL, self.region])
        else:
            metals = findimg_all([img.jiejietupo_img.SINGLE_TARGET.METAL, self.region])
        print([i for i in metals])
        return len([i for i in metals])


    def _check_avaliablilty(self):
        not_fail = self._check_not_failed()
        not_finish = self._check_not_finished()
        return not_finish and not_fail


    def get_name(self):
        x1 = self.region[0] + constants.WINDOW_OFFSET[0]
        y1 = self.region[1] + constants.WINDOW_OFFSET[1]
        x2 = self.region[2] + constants.WINDOW_OFFSET[0]
        y2 = self.region[3] + constants.WINDOW_OFFSET[1]
        img = grab_screen([x1, y1, x2, y2])
        img = Image.fromarray(img)
        name = pytesseract.image_to_string(img, lang='chi_sim')
        self.logger.debug(f'target name: {name}')
        return name


class LiaoTupoTargetsCords(list):
    def __init__(self):
        super().__init__()
        x_start = 651
        y_start = 188
        x_end = 1099
        y_end = 364

        y_add = 369-188
        x_add = 1103 - 651

        start_loc = [x_start+constants.WINDOW_OFFSET[0],
                     y_start+constants.WINDOW_OFFSET[1],
                     x_end+constants.WINDOW_OFFSET[0],
                     y_end+constants.WINDOW_OFFSET[1]]
        for row in range(4):
            for col in range(2):
                cords = [start_loc[0] + x_add*col,
                        start_loc[1] + y_add*row,
                        start_loc[2] + x_add*col,
                        start_loc[3] + y_add*row]
                self.append(cords)



def main_liaotupo():
    '''
    1. 锁定阵容
    2，进入寮突破
    3. 开始挂机
    :return:
    '''
    liao_tupo = LiaoTuPo()
    remain = liao_tupo.get_remain_chance()

    while remain:
        next_target = liao_tupo.get_next_avaliable_target()
        click((int((next_target.region[2] + next_target.region[0])/2),
               int((next_target.region[3] + next_target.region[1])/2)))
        attack_cords = wait_for_state(img.jiejietupo_img.ATTACK)
        click(attack_cords)
        this_fight = combat.Combat('阴阳寮突破', combat_time_limit=60*20)
        combat_result = this_fight.start(auto_ready=True)
        time.sleep(5)
        logging.debug('finished one tupo')
        remain = liao_tupo.get_remain_chance()


# for i in targets_cords:
#     single_target = SingleTarget(i)
#     # o = grab_screen(single_target.region)
#     # o = Image.fromarray(o)
#     # o.show()
#
#
# o = grab_screen([651, 188, 1099, 364])
# o = Image.fromarray(o)
# o.show()
# print(findimg([img.jiejietupo_img.SINGLE_TARGET.FAILED, [651, 188, 1099, 364]]))
# print(pyautogui.locateCenterOnScreen(img.jiejietupo_img.SINGLE_TARGET.FAILED,
#                                      region=[651, 188, 1099, 364],confidence=0.9,grayscale=False))
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