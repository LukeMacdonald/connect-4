class Board:
    def __init__(self, rows, cols):
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def print(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(self.board[row][col], end=' ')
            print()


b = Board(6, 7)
b.print()
