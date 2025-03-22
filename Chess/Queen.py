from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Queen(ChessPiece):
    """
    This class represents a Queen chess piece, inheriting from the base ChessPiece class.
    The Queen can move in straight lines (vertical, horizontal, and diagonal) on the board.
    """
    
    def __init__(self, name, white):
        """
        Initializes the Queen piece with a name and color.
        
        :param name: The name of the Queen.
        :param white: A boolean indicating if the Queen is white (True) or black (False).
        """
        super().__init__(name, white)
    
    def __str__(self):
        """
        Returns a string representation of the Queen piece.
        """
        return super().__str__()

    def getPossibleMoves(self, cordsX, cordsY):
        """
        Returns a list of all possible moves for the Queen based on her current position.
        The Queen moves in all directions: up, down, left, right, and diagonally.
        
        :param cordsX: The current x-coordinate of the Queen.
        :param cordsY: The current y-coordinate of the Queen.
        :return: A list of possible moves for the Queen.
        """
        # This list will hold the possible moves for the Queen.
        ret = []
        
        # Flags to check if the Queen can keep moving in each direction.
        lu = True  # Left-up diagonal
        ru = True  # Right-up diagonal
        ld = True  # Left-down diagonal
        rd = True  # Right-down diagonal
        up = True  # Upward
        down = True  # Downward
        left = True  # Leftward
        right = True  # Rightward

        # Loop through each possible move in all directions.
        for i in range(1, 8):  # Queen can move up to 7 squares in any direction.
            
            # Check if the Queen can move right.
            if right:
                if 0 < cordsY + i < 9:
                    target_piece = ChessBoard.board[cordsX][cordsY + i]

                    # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY + i + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX, chr(cordsY + i + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX, chr(cordsY + i + 64)))
                        right = not right  # Stop moving in this direction

                    else:
                        right = not right  # Stop moving in this direction
            


            # Check if the Queen can move down.
            if down:
                if 0 < cordsX + i < 9:
                    target_piece = ChessBoard.board[cordsX + i][cordsY]

                    # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX + i, chr(cordsY + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX + i, chr(cordsY + 64)))
                            
                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX + i, chr(cordsY + 64)))
                        down = not down  # Stop moving in this direction

                    else:
                        down = not down  # Stop moving in this direction



            # Check if the Queen can move left.
            if left:
                if 0 < cordsY - i < 9:
                    target_piece = ChessBoard.board[cordsX][cordsY - i]

                    # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY - i + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX, chr(cordsY - i + 64)))

                        # Capture opponent's piece
                        else:  
                            ret.append(("e", cordsX, chr(cordsY - i + 64)))
                        left = not left  # Stop moving in this direction

                    else:
                        left = not left  # Stop moving in this direction



            # Check if the Queen can move up.
            if up:
                if 0 < cordsX - i < 9:
                    target_piece = ChessBoard.board[cordsX - i][cordsY]

                      # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX - i, chr(cordsY + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX - i, chr(cordsY + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX - i, chr(cordsY + 64)))
                        up = not up  # Stop moving in this direction

                    else:
                        up = not up  # Stop moving in this direction




            # Check if the Queen can move in the right-down diagonal.
            if rd:
                if 0 < cordsX + i < 9 and 0 < cordsY + i < 9:
                    target_piece = ChessBoard.board[cordsX + i][cordsY + i]

                    # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX + i, chr(cordsY + i + 64))) 

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX + i, chr(cordsY + i + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX + i, chr(cordsY + i + 64))) 
                        rd = not rd  # Stop moving in this direction

                    else:
                        rd = not rd  # Stop moving in this direction




            # Check if the Queen can move in the right-up diagonal.
            if ru:
                if 0 < cordsX - i < 9 and 0 < cordsY + i < 9:
                    target_piece = ChessBoard.board[cordsX - i][cordsY + i]

                     # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX - i, chr(cordsY + i + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX - i, chr(cordsY + i + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX - i, chr(cordsY + i + 64)))
                        ru = not ru  # Stop moving in this direction

                    else:
                        ru = not ru  # Stop moving in this direction




            # Check if the Queen can move in the left-down diagonal.
            if ld:
                if 0 < cordsX + i < 9 and 0 < cordsY - i < 9:
                    target_piece = ChessBoard.board[cordsX + i][cordsY - i]

                    # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX + i, chr(cordsY - i + 64)))

                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX + i, chr(cordsY - i + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX + i, chr(cordsY - i + 64)))
                        ld = not ld  # Stop moving in this direction

                    else:
                        ld = not ld  # Stop moving in this direction




            # Check if the Queen can move in the left-up diagonal.
            if lu:
                if 0 < cordsX - i < 9 and 0 < cordsY - i < 9:
                    target_piece = ChessBoard.board[cordsX - i][cordsY - i]
                    
                     # Move in empty space
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX - i, chr(cordsY - i + 64)))


                    # Capture opponent's King
                    elif not(target_piece.white == self.white):
                        if str(target_piece) == str(King("king", not(self.white))):
                            ret.append(("+", cordsX - i, chr(cordsY - i + 64)))

                        # Capture opponent's piece
                        else:
                            ret.append(("e", cordsX - i, chr(cordsY - i + 64)))
                        lu = not lu  # Stop moving in this direction

                    else:
                        lu = not lu  # Stop moving in this direction
        

        # Return the list of possible moves.
        return ret
