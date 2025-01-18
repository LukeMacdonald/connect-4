class Board:
    def __init__(self, rows, cols):
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        board_str = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                board_str += f"{self.board[row][col]} "
            board_str += "\n"
        return board_str

    def place_token(self, col, token):
        for i in range(len(self.board) - 1, 0, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = token
                return
