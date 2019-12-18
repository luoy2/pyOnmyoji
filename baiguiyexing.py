#!/usr/bin/python3
'''
通过百鬼夜行玩法，自动地撒豆子，获取式神契约碎片

使用ORB算子提取特征匹配已有图像，判断当前状态，然后做出相应动作。

目前还不能邀请好友，不能选定特定的式神，不能调整单次撒豆子个数
'''
import constants
import logging
from ctypes import windll
import time
import numpy as np
import cv2
from grabscreen import grab_screen
from controller import click
from findimg import accept_invite
from utilities import random_sleep
# from transitions import Machine

class BaiguiyexingStateDecision:
    '''
    判定当前百鬼夜行状态的类
    '''
    states = [
        "st_getting_ready",
        "st_choosing_boss",
        # "st_doing_mamemaki",
        "st_getting_bonus"
    ]
    def __init__(self):
        self.logger = logging.getLogger('BaiguiyexingStateDecision')
        img_st_getting_ready = cv2.imread("res/mamemaki/st_getting_ready.jpg")
        img_st_choosing_boss = cv2.imread("res/mamemaki/st_choosing_boss.jpg")
        # img_st_doing_mamemaki = cv2.imread("res/mamemaki/st_doing_mamemaki.jpg")
        img_st_getting_bonus = cv2.imread("res/mamemaki/st_getting_bonus.jpg")

        orb_st_getting_ready = cv2.ORB_create(nfeatures=200, nlevels=4, edgeThreshold=15, 
                                    firstLevel=0, scoreType=cv2.ORB_FAST_SCORE, patchSize=15)
        orb_st_choosing_boss = cv2.ORB_create(nfeatures=1000, nlevels=4, edgeThreshold=15, 
                                    firstLevel=0, scoreType=cv2.ORB_FAST_SCORE, patchSize=15 )
        # orb_st_doing_mamemaki = cv2.ORB_create(nfeatures=1000, nlevels=4, edgeThreshold=15, 
        #                             firstLevel=0, scoreType=cv2.ORB_FAST_SCORE, patchSize=15 )
        orb_st_getting_bonus  = cv2.ORB_create(nfeatures=200, nlevels=4, edgeThreshold=15, 
                                    firstLevel=0, scoreType=cv2.ORB_FAST_SCORE, patchSize=15 )
        
        self.feature_extractors = {
            "st_getting_ready": orb_st_getting_ready,
            "st_choosing_boss": orb_st_choosing_boss,
            # "st_doing_mamemaki": orb_st_doing_mamemaki,
            "st_getting_bonus": orb_st_getting_bonus
        }
        self.descriptors = {
            "st_getting_ready": orb_st_getting_ready.detectAndCompute(img_st_getting_ready, mask=None)[1],
            "st_choosing_boss": orb_st_choosing_boss.detectAndCompute(img_st_choosing_boss, mask=None)[1],
            # "st_doing_mamemaki": orb_st_doing_mamemaki.detectAndCompute(img_st_doing_mamemaki, mask=None)[1],
            "st_getting_bonus": orb_st_getting_bonus.detectAndCompute(img_st_getting_bonus, mask=None)[1]
        }
        self.good_count_thresholds = {
            "st_getting_ready": 10,
            "st_choosing_boss": 20,
            # "st_doing_mamemaki": 5,
            "st_getting_bonus": 10
        }


    def decide(self, in_img):
        '''
        decides if in_img indicates it is in one of the states
        '''
        # brute force 方法找匹配点
        for st in BaiguiyexingStateDecision.states:
            _kp, in_img_des = self.feature_extractors[st].detectAndCompute(in_img, mask=None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            if in_img_des is None or len(in_img_des) == 0:
                continue
            matches = bf.knnMatch(self.descriptors[st], in_img_des, k=2)
            good_count = 0
            try:  # sometimes get ValueError: not enough values to unpack (expected 2, got 1)
                for m,n in matches:
                    if m.distance < 0.50 * n.distance:
                        good_count += 1
                if good_count > self.good_count_thresholds[st]:
                    return st
            except:
                self.logger.warning(f"Got an exeception in self.decide, skipping")
            
        return "st_unknown"


class Baiguiyexing:
    '''
    百鬼夜行自动撒豆
    '''
    def __init__(self):
        self.logger = logging.getLogger('Baiguiyexing')
        # self.machine = Machine(model=self, states=Baiguiyexing.states, initial="st_getting_ready")
        # self.machine.add_transition(trigger="choose_boss", source="st_getting_ready", dest="st_choosing_boss")
        # self.machine.add_transition(trigger="do_mamemaki", source="st_choosing_boss", dest="st_doing_mamemaki")
        # self.machine.add_transition(trigger="get_bonus", source="st_doing_mamemaki", dest="st_getting_bonus")
        # self.machine.add_transition(trigger="get_ready", source="st_getting_bonus", dest="st_getting_ready")
        self.state_judger = BaiguiyexingStateDecision()
        self.win_region = [
            constants.WINDOW_ATTRIBUTES["x_offset"],
            constants.WINDOW_ATTRIBUTES["y_offset"],
            constants.WINDOW_ATTRIBUTES["x_offset"] + constants.WINDOW_ATTRIBUTES["width"],
            constants.WINDOW_ATTRIBUTES["y_offset"] + constants.WINDOW_ATTRIBUTES["height"]
        ]
        self.coord_entry = (
            821 + constants.WINDOW_ATTRIBUTES["x_offset"],
            471 + constants.WINDOW_ATTRIBUTES["y_offset"]
        )   # “进入”按钮的坐标
        self.coord_ok = (
            1055 + constants.WINDOW_ATTRIBUTES["x_offset"],
            553 + constants.WINDOW_ATTRIBUTES["y_offset"]
        )   # “开始”按钮的坐标
        self.coord_leaving = (
            616 + constants.WINDOW_ATTRIBUTES["x_offset"],
            25 + constants.WINDOW_ATTRIBUTES["y_offset"]
        )   # 结算奖励时可点击退出的区域

        # 选择鬼王时三个鬼王的点击坐标
        self.coord_bosses = (
            (
                298 + constants.WINDOW_ATTRIBUTES["x_offset"],
                448 + constants.WINDOW_ATTRIBUTES["y_offset"]
            ),
            (
                572 + constants.WINDOW_ATTRIBUTES["x_offset"],
                482 + constants.WINDOW_ATTRIBUTES["y_offset"]
            ),
            (
                865 + constants.WINDOW_ATTRIBUTES["x_offset"],
                481 + constants.WINDOW_ATTRIBUTES["y_offset"]
            )
        )
    
    ##############################################
    # get current state
    ##############################################
    def get_state(self):
        img_grabbed = grab_screen(region=self.win_region, use_channel_rgb=False)
        _state = self.state_judger.decide(img_grabbed)
        return _state

    ##############################################
    # state transition triggers
    ##############################################
    def get_ready(self):
        for i in range(2):
            # 消抖
            while self.get_state() == "st_getting_ready":
                random_sleep(0.5, 0.5)
                click(self.coord_entry, tired_check=False)
                random_sleep(0.5, 0.5)

    def choose_boss(self):
        for i in range(2):
            # 消抖
            while self.get_state() == "st_choosing_boss":
                # 选择鬼王
                ind = np.random.randint(0, 3)
                click(self.coord_bosses[ind], tired_check=False)
                random_sleep(0.5, 0.5)
                # 点击“开始”
                click(self.coord_ok, tired_check=False)
                random_sleep(0.5, 0.5)

    def do_mamemaki(self):
        self.logger.info("Entered pseudo-state st_doing_mamemaki")
        random_sleep(5)  # 等待先头部队出场

        # 背景剪除
        # there are quite many background removing functions provided by OpenCV
        # try some fast ones?
        bg_substractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

        while self.get_state() not in BaiguiyexingStateDecision.states:
            # 只要没到其他状态就认为砸豆子还在继续
            img_grabbed = grab_screen(region=self.win_region, use_channel_rgb=False)
            fg_mask = bg_substractor.apply(img_grabbed)

            # 消除孤立的细小轮廓
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            # cv2.imwrite("fg_mask.jpg", fg_mask)  # 调试用

            contours, hierarchy	= cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hit_coord = []  # 保存候选点击坐标
            for c in contours:
                # 求轮廓的中心点
                m = cv2.moments(c)
                if abs(m['m00']) < 10000:   # 面积太小则跳过
                    continue
                x = int(m['m10']/m['m00']) + constants.WINDOW_ATTRIBUTES["x_offset"]
                y = int(m['m01']/m['m00']) + constants.WINDOW_ATTRIBUTES["y_offset"]
                hit_coord.append((x, y))
            # print(f"hit_coord is {hit_coord}")
            if len(hit_coord) > 0:
                # 随机选取hit_coord中的一个点进行点击
                ind = np.random.randint(0, len(hit_coord))
                click(hit_coord[ind], tired_check=False)

            random_sleep(0.5, 0.1)


    def get_bonus(self):
        for i in range(2):
            # 消抖
            while self.get_state() == "st_getting_bonus":
                random_sleep(0.5, 0.1)
                click(self.coord_leaving, tired_check=False)
                random_sleep(0.5, 0.1)

    def start(self):
        while True:
            # time_start = cv2.getTickCount()
            state = self.get_state()
            # print(f"used {(cv2.getTickCount() - time_start) / cv2.getTickFrequency() }s")
            self.logger.info(f"Entered state {state}")
            if state == "st_getting_ready":
                self.get_ready()
            elif state == "st_choosing_boss":
                self.choose_boss()
                self.do_mamemaki()
            # elif state == "st_doing_mamemaki":
            #     # 这个状态暂时检测不到
            #     pass
            elif state == "st_getting_bonus":
                self.get_bonus()
            elif state == "st_unknown":
                accept_invite()
            else:
                self.logger.warning(f"Unknown state: {state}")
            time.sleep(2)

def main():

    user32 = windll.user32
    user32.SetProcessDPIAware()

    logging.basicConfig(
        level=0,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S")

    constants.init_constants(u'阴阳师-网易游戏', move_window=False)
    game = Baiguiyexing()
    game.start()
    

if __name__ == "__main__":
    main()