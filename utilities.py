import time
import random
import win32gui

def random_sleep(base=1, multiplier=1):
    time.sleep(base+random.uniform(0,multiplier))


def get_window_info():  # 获取阴阳师窗口信息
    wdname = u'阴阳师-网易游戏'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '小轩提示：请打开PC端阴阳师\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)

def add_pos_with_offset(pos, offset):
    result_list = [0, 0, 0, 0]
    result_list[0] = pos[0] + offset[0]
    result_list[1] = pos[1] + offset[1]
    result_list[2] = pos[2] + offset[0]
    result_list[3] = pos[3] + offset[1]
    return tuple(result_list)
