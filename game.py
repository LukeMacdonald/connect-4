from token import Token

from player import Player
from utils import PlayerColour

ROWS = 6
COLS = 7
TOTAL_TOKENS = (ROWS * COLS) // 2


def create_player(name: str, colour: PlayerColour, num_tokens: int):
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Player(name, colour, tokens)


name1 = input("Enter Player 1 Name: ")
print("Creating Player 1...")
player1 = create_player(name1, PlayerColour.RED, TOTAL_TOKENS)
print(player1)
name2 = input("Enter Player 2 Name: ")
print("Creating Player 2....")
player2 = create_player(name2, PlayerColour.YELLOW, TOTAL_TOKENS)
print(player2)
