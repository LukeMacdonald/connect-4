import math
import random

from objects.board import Board
from objects.enums import PlayerColour, PlayerTypes
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
    def __init__(self, name, colour, tokens, depth):
        super().__init__(name, colour, tokens)
        self.depth = depth

    def minimax(
        self,
        board,
        depth,
        alpha,
        beta,
        maximizing_player,
        computer_colour,
        player_colour,
    ):
        if depth == 0 or board.is_terminal_state():
            return board.evaluate_board(computer_colour, player_colour)
        if maximizing_player:
            max_eval = -math.inf
            for col in range(board.cols):
                if board.is_valid_column(col, PlayerTypes.COMPUTER):
                    temp_board = board.copy()
                    row, _ = temp_board.place_token(Token(computer_colour, True), col)
                    eval_score = self.minimax(
                        temp_board,
                        depth - 1,
                        alpha,
                        beta,
                        False,
                        computer_colour,
                        player_colour,
                    )
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, max_eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for col in range(board.cols):
                if board.is_valid_column(col, PlayerTypes.COMPUTER):
                    # Simulate placing the player's token
                    temp_board = board.copy()
                    row, _ = temp_board.place_token(Token(PlayerColour.RED, True), col)
                    eval_score = self.minimax(
                        temp_board,
                        depth - 1,
                        alpha,
                        beta,
                        True,
                        computer_colour,
                        player_colour,
                    )
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval

    def best_move(self, board: Board):
        best_score = -math.inf
        best_col = random.choice(range(board.cols))
        for col in range(board.cols):
            if board.is_valid_column(col, PlayerTypes.COMPUTER):
                temp_board = board.copy()
                row, _ = temp_board.place_token(Token(self.colour, True), col)
                score = self.minimax(
                    temp_board,
                    self.depth,
                    -math.inf,
                    math.inf,
                    False,
                    PlayerColour.YELLOW,
                    PlayerColour.RED,
                )  # todo: implemented minimax
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col
