from enum import Enum


class PlayerColour(Enum):
    RED = 1
    YELLOW = 2


def token_from_dict(data):
    if data["colour"] == PlayerColour.RED.name:
        return PlayerColour.RED
    return PlayerColour.YELLOW
