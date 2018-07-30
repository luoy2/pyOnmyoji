import time
import random
import win32gui

def random_sleep():
    time.sleep(1+random.uniform(0,1))


def get_window_info():  # 获取阴阳师窗口信息
    wdname = u'阴阳师-网易游戏'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '小轩提示：请打开PC端阴阳师\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)
