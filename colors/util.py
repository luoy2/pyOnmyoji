from grabscreen import grab_screen
from PIL import Image


def normalize_color_list(color_list):
    result_list = []
    start_x, start_y = color_list[0][0]
    for i in color_list:
        offset_x = i[0][0] - start_x
        offset_y = i[0][1] - start_y
        offset_color = i[1]
        result_list.append([(offset_x, offset_y), offset_color])
    return result_list


class ColorToMatch:
    def __init__(self, region, color_list, tolerance):
        self.color_list = color_list
        self.tolerance = tolerance
        self.region = region
        self.screen_shot_region = self.get_region_to_screenshot()


    def show(self):
        region_img = Image.fromarray(grab_screen(region=self.region), mode='RGB')
        region_img.show()

    def get_region_to_screenshot(self):
        min_x = min(i[0][0] for i in self.color_list) - 10
        min_y = min(i[0][1] for i in self.color_list) - 10
        max_x = max(i[0][0] for i in self.color_list) + 10
        max_y = max(i[0][1] for i in self.color_list) + 10
        x0 = max(min(self.region[0], self.region[0] + min_x), 0)
        y0 = max(min(self.region[1], self.region[1] + min_y), 0)
        x1 = max(self.region[2], self.region[2] + max_x)
        y1 = max(self.region[3], self.region[3] + max_y)
        return (x0, y0, x1, y1)

raw_accept_invite = [[(1142, 607), (97, 186, 108)],
                     [(1169, 588), (97, 187, 108)],
                     [(1127, 599), (95, 185, 106)]]


class UtilColor:
    AcceptInvite = ColorToMatch((1095, 544, 1202, 655), normalize_color_list(raw_accept_invite), 1)


raw_find_chaoguiwang = [[(28, 366), (227, 217, 205)],
                        [(59, 397), (208, 140, 64)],
                        [(85, 406), (132, 110, 92)],
                        [(23, 445), (221, 211, 198)]]


class ChaoGuiColor:
    FindChaoGui = ColorToMatch((19, 352, 116, 464), normalize_color_list(raw_find_chaoguiwang), 1)


raw_start = [((1391, 826), (243, 178, 94)), ((1383, 910), (167, 155, 145)), ((1486, 851), (243, 178, 94))]


class PartyColor:
    StartFight = ColorToMatch((1250, 816, 1508, 895), normalize_color_list(raw_start), 1)



raw_win = [((652, 261), (131, 26, 17)), ((685, 313), (152, 27, 17)), ((658, 341), (213, 199, 177)), ((612, 300),
           (145, 26, 17))]
raw_lose = [((638, 245), (84, 78, 96)),((678, 300), (91, 82, 101)), ((644, 335), (196, 178, 151)), ((609,297), (91, 82, 101))]
raw_guihuo = [((1185, 993), (255, 255, 255)), ((1184, 964), (2, 110, 177)), ((1188, 995), (253, 254, 255))]
# damo = [((858, 756), (46, 26, 20)), ((827, 729), (189, 82, 42)), ((916, 746), (187, 60, 26)), ((909, 799), (14, 1, 1))]
damo = [[(969, 869), (55, 2, 4)], [(1031, 838), (111, 41, 11)], [(958, 843), (127, 14, 14)]]
raw_ready = [[(1525, 764), (255, 243, 209)], [(1569, 776), (212, 174, 119)], [(1600, 801), (255, 242, 208)], [(1658, 899), (199, 42, 19)]]
class CombatColor:
    Ready = ColorToMatch((1508, 741, 1568, 814), normalize_color_list(raw_ready), 2)
    InCombat = ColorToMatch((703, 955, 1200, 1010), normalize_color_list(raw_guihuo), 1)
    Win = ColorToMatch((610-50, 213-50-50, 660+50, 272+50), normalize_color_list(raw_win), 1)
    Lose = ColorToMatch((610-50, 213-50-50, 660+50, 272+50), normalize_color_list(raw_lose), 1)
    # Damo = ColorToMatch((858-50, 756-50, 858+50, 756+50), normalize_color_list(damo), 1)
    Damo = ColorToMatch((960, 629, 980, 959), normalize_color_list(damo), 1)






raw_map = [(164, 944), (160, 105, 43)], [(113, 930), (87, 30, 94)], [(180, 940), (154, 99, 37), 2]
raw_main = [[(1674, 900), (222, 205, 200)], [(1681, 832), (207, 167, 109)], [(1676, 976), (193, 86, 77)]]
raw_jiejie = [[(837, 122), (248, 243, 224)]]
class LocatorColor:
    Map = ColorToMatch((164-5, 944-5, 164+5, 944+5), normalize_color_list(raw_map), 2)
    Main = ColorToMatch((1674-5, 900-5, 1674+5, 900+5), normalize_color_list(raw_main), 2)
    Jiejie = ColorToMatch((836, 121, 838, 123), normalize_color_list(raw_jiejie), 0)



class JiejieColor:
    LiaoAttack = ColorToMatch([537, 169, 1459, 963], [[(0, 0), (243, 178, 94)], [(33, -37), (150, 59, 46)], [(-331, -3), (243, 178, 94)]], 1)
    PersonalAttack = ColorToMatch([163, 165, 1565, 964], [[(0, 0), (243, 178, 94)], [(78, -32), (151, 60, 46)], [(-80, 33), (152, 61, 46)]], 1)