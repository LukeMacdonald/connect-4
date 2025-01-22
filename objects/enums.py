from enum import Enum


class PlayerColour(Enum):
    RED = 1
    YELLOW = 2


class GameOptions(Enum):
    OFFLINE = 1
    ONLINE = 2
    JOIN = 3
    COMPUTER = 4


class PlayerTypes(Enum):
    PLAYER = 1
    COMPUTER = 2
