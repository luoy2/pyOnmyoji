from utilities import resolution
import enum

resolution = resolution()
if resolution == (1920, 1080):
    RES_PATH = 'res1080p'
else:
    RES_PATH = 'res'


GAMBLE_MAIN = [RES_PATH + '/gamble/gamble.png', (78, 170, 1085, 413)]
GAMBLE_DASH = [RES_PATH + '/gamble/gamble_dash.png', (500, 100, 700, 200)]
RED = [RES_PATH + '/gamble/red.png', (900, 500, 1200, 700)]
BLUE = [RES_PATH + '/gamble/blue.png', (900, 500, 1200, 700)]
NEXT = [RES_PATH + '/gamble/next.png', (460, 420, 730, 630)]