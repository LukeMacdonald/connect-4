from token import Token

from board import Board
from player import Player
from utils import PlayerColour

ROWS = 6
COLS = 7
TOTAL_TOKENS = (ROWS * COLS) // 2


def create_player(name: str, colour: PlayerColour, num_tokens: int):
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Player(name, colour, tokens)


def swap_player(current, other):
    return other, current


def init_game():
    name1 = input("Enter Player 1 Name: ")
    print("Creating Player 1...")
    player1 = create_player(name1, PlayerColour.RED, TOTAL_TOKENS)
    print(player1)
    name2 = input("Enter Player 2 Name: ")
    print("Creating Player 2....")
    player2 = create_player(name2, PlayerColour.YELLOW, TOTAL_TOKENS)
    print(player2)
    board = Board(ROWS, COLS)
    print(board)
    return player1, player2, board


def play_game(p1, p2, board):
    current_player = p1
    other_player = p2
    while current_player.has_tokens() or other_player.has_tokens():
        if not current_player.has_tokens():
            current_player, other_player = swap_player(current_player, other_player)
        else:
            token = current_player.remove_token()
            print(board)
            selected_col = int(input("Enter Column to place token: "))
            while selected_col < 0 or selected_col > COLS - 1:
                selected_col = int(input("Enter Column to place token: "))
            board.place_token(selected_col, token)
            current_player, other_player = swap_player(current_player, other_player)
            print(current_player)


p1, p2, board = init_game()
play_game(p1, p2, board)
