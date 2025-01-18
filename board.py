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
                return True
        return False
