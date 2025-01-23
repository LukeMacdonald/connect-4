from objects.enums import PlayerColour
from objects.player import Computer, Player
from objects.token import Token


def create_player(name: str, colour: PlayerColour, num_tokens: int):
    """
    Create a player with the specified name, colour, and number of tokens.
    """
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Player(name, colour, tokens)


def create_computer(num_tokens: int):
    colour = PlayerColour.YELLOW
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Computer("AI", colour, tokens, 4)


def swap_player(current, other):
    """
    Swap the current player with the other player.
    """
    return other, current
