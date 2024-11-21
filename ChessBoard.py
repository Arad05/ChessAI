class ChessBoard:
    def __init__(self):
        # Initialize a 9x9 board with spaces
        self.board = [[" " for _ in range(9)] for _ in range(9)]

    def setBoard(self):
        # Label the top row with A-H
        for i in range(1, len(self.board[0])):
            self.board[0][i] = chr(ord('A') + i - 1)+" "
        # Label the left column with 1-8
        for i in range(1, len(self.board)):
            self.board[i][0] = str(i)
        # Put dots as blank spaces
        for i in range(1, len(self.board)):
            for j in range(1, len(self.board[i])):
                self.board[i][j] = ". "
        
    def movePiece(self, rowXO, colYO, rowXN, colYN):
        # Convert board coordinates to indices
        old_row = rowXO
        old_col = ord(colYO.upper()) - 64  # 'A' -> 1, 'B' -> 2, ...
        new_row = rowXN
        new_col = ord(colYN.upper()) - 64

        # Validate indices
        if not (1 <= old_row <= 8 and 0 <= old_col <= 7 and 1 <= new_row <= 8 and 0 <= new_col <= 7):
            raise ValueError("Invalid move coordinates. Rows must be 1-8, and columns A-H.")

        # Perform the move
        self.board[new_row][new_col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = ". "  # Empty the original square

    def display(self):
        # Convert the board into a string for display
        ret = ""
        for row in self.board:
            ret += " ".join(row) + "\n"
        return ret


# Create and prepare the chessboard
board = ChessBoard()
board.setBoard()
board.board[5][5]="K "
board.board[3][4]="q "
print(board.display())
board.movePiece(5,"e", 3, "D")
print(board.display())
board.movePiece( 3, "D",5,"C")
print(board.display())
