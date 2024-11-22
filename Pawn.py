from ChessPiece import ChessPiece
from ChessBoard import ChessBoard

class Pawn(ChessPiece):
    
    def __init__(self,name,white):
        super().__init__(name, white)
        counter =0
    
    def __str__(self):
        return super().__str__()
        

    def possibleMoves(self,cordsX,cordsY):
        ret = []
        # Normal moves for white
        if self.white:
            if self.countre ==0:
                if ChessBoard.board[cordsX][cordsY+2] == " . ":
                    ret.append((ord(cordsX+64),cordsY+2))
            if ChessBoard.board[cordsX][cordsY+1] == " . ":
                ret.append((ord(cordsX+64),cordsY+1))
        return ret