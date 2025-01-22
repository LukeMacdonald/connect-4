import math
import random

from objects.board import Board
from objects.enums import PlayerColour
from objects.helpers import copy_board
from objects.token import Token


class Player:
    def __init__(self, name: str, colour: PlayerColour, tokens: list):
        self.name = name
        self.colour = colour
        self.tokens = tokens

    def __str__(self):
        name = f"Name: {self.name}"
        colour = f"Color: {self.colour.name}"
        total_tokens = f"Tokens Left: {len(self.tokens)}"
        return f"{name}\n{colour}\n{total_tokens}"

    def to_dict(self):
        return {
            "name": self.name,
        }

    def remove_token(self):
        return self.tokens.pop(0)

    def has_tokens(self):
        return len(self.tokens) > 0


class Computer(Player):
    def best_move(self, board: Board):
        best_score = -math.inf
        best_col = random.choice(range(board.cols))
        for col in range(board.cols):
            if board.is_valid_column(col):
                temp_board = copy_board(board)
                row, _ = temp_board.place_token(Token(self.colour, True), col)
                score = -math.inf  # todo: implemented minimax
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col
