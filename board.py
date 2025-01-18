from utils import PlayerColour


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        board_str = ""
        for col in range(self.cols):
            board_str += f"{col} "
        board_str += "\n" + "--" * self.cols + "\n"
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                board_str += f"{self.board[row][col]} "
            board_str += "\n"
        return board_str

    def check_col(self, col):
        if col < 0 or col > self.cols - 1:
            print("Column selected must be between 0 and {self.cols - 1}")
            return False
        if self.board[0][col] != 0:
            print("Select Colum is full")
            return False
        return True

    def place_token(self, token):
        selected_col = int(input("Enter Column to place token: "))
        while not self.check_col(selected_col):
            selected_col = int(input("Enter Column to place token: "))

        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i][selected_col] == 0:
                self.board[i][selected_col] = token
                return i, selected_col
        return -1, -1

    def check(self, row, col, colour):

        def check_vertical():
            count = 0
            for i in range(len(self.board)):
                if self.board[i][col] == 0:
                    count = 0
                else:
                    if self.board[i][col].colour == colour:
                        count += 1
                    else:
                        count = 0
                if count == 4:
                    return True
            return count == 4

        def check_horizontal():
            count = 0
            for i in range(len(self.board[row])):
                if self.board[row][i] == 0:
                    count = 0
                else:
                    if self.board[row][i].colour == colour:
                        count += 1
                    else:
                        count = 0
                if count == 4:
                    return True
            return count == 4

        def check_space(temp_row, temp_col, x_step, y_step, count):
            curr_row = temp_row + y_step
            curr_col = temp_col + x_step
            if (
                curr_row >= 0
                and curr_col >= 0
                and curr_row < self.rows
                and curr_col < self.cols
            ):
                curr_space = self.board[curr_row][curr_col]
                if curr_space != 0 and curr_space.colour == colour:
                    count += 1
                    return check_space(curr_row, curr_col, x_step, y_step, count)
                return count
            else:
                return count

        def check_diagonally():
            count = (
                1 + check_space(row, col, 1, -1, 0) + check_space(row, col, -1, 1, 0)
            )
            if count >= 4:
                return True

            count = (
                1 + check_space(row, col, -1, -1, 0) + check_space(row, col, 1, 1, 0)
            )
            if count >= 4:
                return True

        if check_diagonally():
            return True
        if check_vertical():
            return True

        if check_horizontal():
            return True

        return False
