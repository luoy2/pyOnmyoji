import enum
PARTY_CONTAINER_CORDS = (150, 150, 550, 1000)

MAIN_TUPO = ['res/jiejietupo/main.png', (0, 0, 1700, 200)]
REFRESH_WAITING = ['res/party/refresh_waiting.png', (1018, 511, 1012, 547)]
REFRESH = ['res/party/refresh.png', (500, 700, 800, 1000)]
YAOQIFENGYIN = ['res/party/yaoqifengyin.png', PARTY_CONTAINER_CORDS]



class SINGLE_TARGET:
    FINISHED = 'res/jiejietupo/finished.png'
    FAILED = 'res/jiejietupo/failed.png'
    METAL = 'res/jiejietupo/metal.png'
    FINISHED_METAL = 'res/jiejietupo/finished_metal.png'

class PARTY_CORDS(enum.Enum):
    YAOQIFENGYIN = (345, 839)


