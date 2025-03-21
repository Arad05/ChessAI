from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Rook(ChessPiece):
    """
    Represents a Rook chess piece. Inherits from the ChessPiece class.
    The Rook can move in straight lines (horizontally or vertically) across the board.
    """

    def __init__(self, name, white):
        """
        Initializes the Rook object.
        
        :param name: Name of the rook piece (e.g., 'Rook').
        :param white: Boolean indicating if the piece is white (True) or black (False).
        """
        super().__init__(name, white)
        
        # Flag indicating if the rook has moved (used for castling)
        self.moved = False  
    
    def __str__(self):
        """
        Returns a string representation of the Rook piece.
        
        :return: String representation of the Rook, inherited from the parent class.
        """
        return super().__str__()
    
    def getPossibleMoves(self, cordsX, cordsY):
        """
        Gets the possible moves for the Rook from its current position.
        The Rook moves in a straight line either horizontally or vertically.
        
        :param cordsX: The X-coordinate (row) of the Rook's current position.
        :param cordsY: The Y-coordinate (column) of the Rook's current position.
        :return: A list of tuples representing possible moves. Each tuple contains:
                 - A flag ('e' for enemy capture, '+' for attacking a King, '' for normal move)
                 - The new X-coordinate
                 - The new Y-coordinate (as a letter from 'A' to 'H')
        """
        
        ret = []  # List to store possible moves
        
        # Flags indicating movement directions
        up = True
        down = True
        left = True
        right = True

        # The Rook can move up to 7 squares in each direction (up, down, left, right)
        for i in range(1, 8):
            
            # Moving right
            if right:
                if 0 < cordsY + i < 9:
                    
                    target_piece = ChessBoard.board[cordsX][cordsY + i]
                    
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY + i + 64)))  # Normal move
                    
                    elif target_piece.white != self.white:
                        if str(target_piece) == str(King("king", not self.white)):
                            ret.append(("+", cordsX, chr(cordsY + i + 64)))  # Attack on opponent's King
                        else:
                            ret.append(("e", cordsX, chr(cordsY + i + 64)))  # Capture an enemy piece
                        
                        right = False  # Stop looking further in this direction
                    
                    else:
                        right = False  # Stop if blocked by a piece of the same color

            # Moving down
            if down:
                if 0 < cordsX + i < 9:
                    
                    target_piece = ChessBoard.board[cordsX + i][cordsY]
                    
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX + i, chr(cordsY + 64)))  # Normal move
                    
                    elif target_piece.white != self.white:
                        if str(target_piece) == str(King("king", not self.white)):
                            ret.append(("+", cordsX + i, chr(cordsY + 64)))  # Attack on opponent's King
                        else:
                            ret.append(("e", cordsX + i, chr(cordsY + 64)))  # Capture an enemy piece
                        
                        down = False  # Stop looking further in this direction
                    
                    else:
                        down = False  # Stop if blocked by a piece of the same color

            # Moving left
            if left:
                if 0 < cordsY - i < 9:
                    
                    target_piece = ChessBoard.board[cordsX][cordsY - i]
                    
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY - i + 64)))  # Normal move
                    
                    elif target_piece.white != self.white:
                        if str(target_piece) == str(King("king", not self.white)):
                            ret.append(("+", cordsX, chr(cordsY - i + 64)))  # Attack on opponent's King
                        else:
                            ret.append(("e", cordsX, chr(cordsY - i + 64)))  # Capture an enemy piece
                        
                        left = False  # Stop looking further in this direction
                    
                    else:
                        left = False  # Stop if blocked by a piece of the same color

            # Moving up
            if up:
                if 0 < cordsX - i < 9:
                    
                    target_piece = ChessBoard.board[cordsX - i][cordsY]
                    
                    if str(target_piece) == str(ChessBoard.null()):
                        ret.append(("", cordsX - i, chr(cordsY + 64)))  # Normal move
                    
                    elif target_piece.white != self.white:
                        if str(target_piece) == str(King("king", not self.white)):
                            ret.append(("+", cordsX - i, chr(cordsY + 64)))  # Attack on opponent's King
                        else:
                            ret.append(("e", cordsX - i, chr(cordsY + 64)))  # Capture an enemy piece
                        
                        up = False  # Stop looking further in this direction
                    
                    else:
                        up = False  # Stop if blocked by a piece of the same color

        return ret  # Return the list of possible moves
