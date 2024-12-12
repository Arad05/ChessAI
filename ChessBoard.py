class ChessBoard:
    # Class-level board definition
    board = [[" " for _ in range(9)] for _ in range(9)]
    pieces = []

    @staticmethod
    class null:
        
        @staticmethod
        def __str__():  # Added colon here
            return " . "


    @staticmethod
    def makeBoard():
        # Label the top row with A-H
        for i in range(1, len(ChessBoard.board[0])):
            ChessBoard.board[0][i] = " "+chr(ord('A') + i - 1) + " "
        # Label the left column with 1-8
        for i in range(1, len(ChessBoard.board)):
            ChessBoard.board[i][0] = str(i)
        # Put dots as blank spaces
        for i in range(1, len(ChessBoard.board)):
            for j in range(1, len(ChessBoard.board[i])):
                ChessBoard.board[i][j] = ChessBoard.null()


    @staticmethod
    def movePiece(rowXO, colYO, rowXN, colYN):
        # Convert board coordinates to indices
        old_row = int(rowXO)
        old_col = ord(colYO.upper()) - 64  # 'A' -> 1, 'B' -> 2, ...
        new_row = int(rowXN)
        new_col = ord(colYN.upper()) - 64

        # Validate indices
        if not (1 <= old_row <= 8 and 1 <= old_col <= 8 and 1 <= new_row <= 8 and 1 <= new_col <= 8):
            raise ValueError("Invalid move coordinates. Rows must be 1-8, and columns A-H.")

        # Perform the move
        if not(ChessBoard.board[old_row][old_col]==str(ChessBoard.null())):
            ChessBoard.board[new_row][new_col] = ChessBoard.board[old_row][old_col]
            ChessBoard.board[old_row][old_col] = str(ChessBoard.null())  # Empty the original square
            for piece in ChessBoard.pieces:
                
                if not(piece[1][0] ==rowXO and chr(piece[1][1]+64) ==colYO.upper()):
                    continue

                piece[1]=[new_row,new_col]


    @staticmethod
    def putThePieceDown(piece, cords):
        # `cords` should be a tuple (row, column) 
        row = cords[0]
        col = cords[1] 
        ChessBoard.board[row][col] = piece
        ChessBoard.pieces.append([piece,[row,col]])

    @staticmethod
    def deleteThePiece(cords):
        # `cords` should be a tuple (row, column) 
        row = cords[0]
        col = cords[1] 
        ChessBoard.pieces.remove([ChessBoard.board[row][col],[row,col]])
        ChessBoard.board[row][col] = ChessBoard.null()
        


    @staticmethod
    def __str__():
        # Convert the board into a string for display
        ret = ""
        for row in ChessBoard.board:
            for place in row:
                ret+=str(place)
            ret+="\n"
        return ret+"\n"
    

