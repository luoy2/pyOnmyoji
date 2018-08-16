import time
import random
import win32gui
import struct



def hex2rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val for val in int_tuple])


def random_sleep(base=1, multiplier=1):
    time.sleep(base+random.uniform(0,multiplier))


def get_window_info(wdname = u'阴阳师-网易游戏'):  # 获取阴阳师窗口信息
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





def cordinates_convert(cords, original_scale=(2048,1536), current_res=get_window_info()[2:]):
    new_x = cords[0]*original_scale[0]/current_res[0]
    new_y = cords[0]*original_scale[1]/current_res[1]
    return (new_x, new_y)


