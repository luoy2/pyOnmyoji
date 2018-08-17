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
        self.region = region
        self.color_list = color_list
        self.tolerance = tolerance

    def show(self):
        region_img = Image.fromarray(grab_screen(region=self.region), mode='RGB')
        region_img.show()


raw_accept_invite = [[(1142, 607), (97, 186, 108)],
                     [(1169, 588), (97, 187, 108)],
                     [(1127, 599), (95, 185, 106)],
                     [(1145, 580), (49, 31, 29)]]


class UtilColor:
    AcceptInvite = ColorToMatch((1095, 544, 1202, 655), normalize_color_list(raw_accept_invite), 1)


raw_find_chaoguiwang = [[(28, 366), (227, 217, 205)],
                        [(59, 397), (208, 140, 64)],
                        [(85, 406), (132, 110, 92)],
                        [(23, 445), (221, 211, 198)]]


class ChaoGuiColor:
    FindChaoGui = ColorToMatch((19, 352, 116, 464), normalize_color_list(raw_find_chaoguiwang), 1)






raw_start = [((1391, 826), (243, 178, 94)),((1383, 910), (167, 155, 145)),((1486, 851), (243, 178, 94))]

class PartyColor:
    StartFight = ColorToMatch((1277, 816, 1508, 895), normalize_color_list(raw_start), 1)



raw_guihuo = [((1185, 993), (255, 255, 255)),((1184, 964), (2, 110, 177)),((1188, 995), (253, 254, 255))]
class CombatColor:
    InCombat = ColorToMatch((1172, 955, 1200, 1010), normalize_color_list(raw_guihuo), 2)