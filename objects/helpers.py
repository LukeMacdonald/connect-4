from objects.board import Board
from objects.enums import PlayerColour
from objects.player import Computer, Player
from objects.token import Token


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


def create_computer(num_tokens: int):
    colour = PlayerColour.YELLOW
    tokens = [Token(colour, False) for _ in range(num_tokens)]
    return Computer("AI", colour, tokens)


def swap_player(current, other):
    """
    Swap the current player with the other player.
    """
    return other, current


def copy_board(board):
    """Create a deep copy of the board."""
    new_board = Board(board.rows, board.cols)
    new_board.from_dict(board.to_dict()["board"])
    return new_board


def evaluate_board(board, computer_token, player_token):
    score = 0

    def count_tokens(line):
        computer_count = line.count(computer_token)
        player_count = line.count(player_token)
        if computer_count > player_count:
            return 10**computer_count
        elif player_count > 0 and computer_count == 0:  # Only player tokens in the line
            return -(10**player_count)
        return 0

    for row in range(board.rows):
        for col in range(board.cols):
            if col + 3 < board.cols:
                # Horizontal
                line = [
                    (
                        board.board[row][col + i].colour
                        if board.board[row][col + i] != 0
                        else None
                    )
                    for i in range(4)
                ]
            if row + 3 < board.rows:
                # Vertical
                line = [
                    (
                        board.board[row + i][col].colour
                        if board.board[row + i][col] != 0
                        else None
                    )
                    for i in range(4)
                ]
                score += count_tokens(line)
                if col + 3 < board.cols and row + 3 < board.rows:
                    # Diagonal (top-left to bottom-right)
                    line = [
                        (
                            board.board[row + i][col + i].colour
                            if board.board[row + i][col + i] != 0
                            else None
                        )
                        for i in range(4)
                    ]
                    score += count_tokens(line)
                if col - 3 >= 0 and row + 3 < board.rows:
                    # Diagonal (top-right to bottom-left)
                    line = [
                        (
                            board.board[row + i][col - i].colour
                            if board.board[row + i][col - i] != 0
                            else None
                        )
                        for i in range(4)
                    ]
                    score += count_tokens(line)

        return score
