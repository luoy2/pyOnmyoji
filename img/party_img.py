import enum
PARTY_CONTAINER_CORDS = (150, 150, 550, 1000)

MAIN_PARTY = ['res/party/main_party.png', (0, 700, 1700, 1100)]
REFRESH_WAITING = ['res/party/refresh_waiting.png', (1018, 511, 1012, 547)]
REFRESH = ['res/party/refresh.png', (500, 700, 800, 1000)]
YAOQIFENGYIN = ['res/party/yaoqifengyin.png', PARTY_CONTAINER_CORDS]


class PARTY_CORDS(enum.Enum):
    YAOQIFENGYIN = (345, 839)