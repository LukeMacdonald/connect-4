from objects.helpers import token_from_dict
from objects.token import Token


class Board:
    WIN_CONDITION = 4  # Number of tokens needed to win

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        board_str = "  ".join(map(str, range(self.cols))) + "\n"  # Column numbers
        board_str += "--" * self.cols + "\n"  # Separator
        for row in self.board:
            board_str += "  ".join(str(cell) if cell else "." for cell in row) + "\n"
        return board_str

    def to_dict(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "board": [
                [cell.to_dict() if isinstance(cell, Token) else cell for cell in row]
                for row in self.board
            ],
        }

    def from_dict(self, new_board):
        self.board = [
            [
                Token(token_from_dict(cell), True) if isinstance(cell, dict) else cell
                for cell in row
            ]
            for row in new_board
        ]

    def is_valid_column(self, col):
        """Check if the column is within range and not full."""
        if col < 0 or col >= self.cols:
            print(f"Column must be between 0 and {self.cols - 1}.")
            return False
        if self.board[0][col] != 0:
            print("Column is full. Choose a different column.")
            return False
        return True

    def place_token(self, token, selected_col):
        for row in range(self.rows - 1, -1, -1):  # Start from the bottom
            if self.board[row][selected_col] == 0:
                self.board[row][selected_col] = token
                return row, selected_col
        return -1, -1

    def players_turn(self, token, player):
        """Place a token in the selected column and return its position."""
        while True:
            try:
                selected_col = int(
                    input(f"{player}, choose a column (0-{self.cols - 1}): ")
                )
                if self.is_valid_column(selected_col):
                    break
            except ValueError:
                print("Invalid input. Please enter a valid column number.")
        return self.place_token(token, selected_col)

    def check(self, row, col, colour):
        """Check if placing a token at (row, col) results in a win."""

        def count_consecutive_tokens(x_step, y_step):
            """Count consecutive tokens in one direction (x_step, y_step)."""
            count = 0
            curr_row, curr_col = row + y_step, col + x_step
            while 0 <= curr_row < self.rows and 0 <= curr_col < self.cols:
                cell = self.board[curr_row][curr_col]
                if cell != 0 and cell.colour == colour:
                    count += 1
                    curr_row += y_step
                    curr_col += x_step
                else:
                    break
            return count

        def has_win():
            """Check all directions for a win."""
            # Vertical (up and down)
            vertical_count = (
                1 + count_consecutive_tokens(0, 1) + count_consecutive_tokens(0, -1)
            )
            if vertical_count >= self.WIN_CONDITION:
                return True

            # Horizontal (left and right)
            horizontal_count = (
                1 + count_consecutive_tokens(1, 0) + count_consecutive_tokens(-1, 0)
            )
            if horizontal_count >= self.WIN_CONDITION:
                return True

            # Diagonal (top-left to bottom-right)
            diag1_count = (
                1 + count_consecutive_tokens(1, 1) + count_consecutive_tokens(-1, -1)
            )
            if diag1_count >= self.WIN_CONDITION:
                return True

            # Diagonal (top-right to bottom-left)
            diag2_count = (
                1 + count_consecutive_tokens(-1, 1) + count_consecutive_tokens(1, -1)
            )
            if diag2_count >= self.WIN_CONDITION:
                return True

            return False

        return has_win()
