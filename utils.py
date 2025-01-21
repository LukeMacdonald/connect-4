from token import Token

from player import Player
from player_colour import PlayerColour

ROWS = 6
COLS = 7
TOTAL_TOKENS = (ROWS * COLS) // 2


def token_from_dict(data):
    if data["colour"] == PlayerColour.RED.name:
        return PlayerColour.RED
    return PlayerColour.YELLOW


def create_player(name: str, colour: PlayerColour, num_tokens: int):
    """
    Create a player with the specified name, colour, and number of tokens.
    """
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Player(name, colour, tokens)
