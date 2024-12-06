from ChessPiece import ChessPiece
from ChessBoard import ChessBoard

class King(ChessPiece):
    
    def __init__(self,name,white):
        super().__init__(name, white)
    
    def __str__(self):
        return super().__str__()
        

    def getPossibleMoves(self,cordsX,cordsY):
        ret = []
        
        # Moves for white
        if self.white: 
            moves = [
                (-1, -1), (-1,0), (-1, 1), 
                (0, -1), (0, 1),
                (1, -1), (1,0), (1, 1),
            ]
        else:
            moves = [
                (1, -1), (1,0), (1, 1),
                (0, -1), (0, 1),
                (-1, -1), (-1,0), (-1, 1), 
            ]
        
        for dx, dy in moves:
            new_x, new_y = cordsX + dx, cordsY + dy
            
            # Check if move is within board boundaries
            if 0 < new_x < 9 and 0 < new_y < 9:
                # Check if square is empty
                if str(ChessBoard.board[new_x][new_y]) == str(ChessBoard.null()):
                    ret.append(("", new_x, chr(new_y+64)))
                elif not(ChessBoard.board[new_x][new_y].white == self.white):
                    if isinstance(ChessBoard.board[new_x][new_y], King):
                        ret.append(("+", new_x, chr(new_y+64)))
                    else:
                        ret.append(("e", new_x, chr(new_y+64)))
        return ret