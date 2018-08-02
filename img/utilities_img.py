from utilities import resolution
import enum
resolution = resolution()
if resolution == (1920, 1080):
    RES_PATH = 'res1080p'
else:
    RES_PATH = 'res'


NOT_ENOUGH_SUSHI = [RES_PATH + 'utilities/not_enough_sushi.png', (820, 450, 1030, 600)]
RED_CROSS = [RES_PATH + '/utilities/red_cross.png', (0, 0, 1300, 800)]