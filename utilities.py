import time
import random
import win32gui
import struct
import logging

_original_scale={'width': 1704, 'height': 960, 'x_offset': 12, 'y_offset': 47}


def hex2rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val for val in int_tuple])


def random_sleep(base=1, multiplier=1):
    sleep_time = base+random.uniform(0,multiplier)
    logging.debug(f'random sleep time {sleep_time} seconds...')
    time.sleep(sleep_time)


def get_window_info(wdname = u'阴阳师-网易游戏'):  # 获取阴阳师窗口信息
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '小轩提示：请打开PC端阴阳师\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)

def add_pos_with_offset(pos, _current_scale):
    result_list = [0, 0, 0, 0]
    result_list[:2] = cordinates_convert((pos[0], pos[1]), _current_scale)
    result_list[2:] = cordinates_convert((pos[2], pos[3]), _current_scale)
    return tuple(result_list)



def cordinates_convert(cords, _current_scale):
    global _original_scale
    new_x = int((cords[0]-_original_scale['x_offset']) / _original_scale['width'] * _current_scale['width']) + _current_scale['x_offset']
    new_y = int((cords[1]-_original_scale['y_offset']) / _original_scale['height'] * _current_scale['height']) + _current_scale['y_offset']
    return (new_x, new_y)



def cordinates_scale(cords, _current_scale):
    global _original_scale
    new_x = int((cords[0]) / _original_scale['width'] * _current_scale['width'])
    new_y = int((cords[1]) / _original_scale['height'] * _current_scale['height'])
    return (new_x, new_y)


