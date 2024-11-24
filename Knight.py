from ChessPiece import ChessPiece
from ChessBoard import ChessBoard

class Knight(ChessPiece):

    def __init__(self,name,white):
        super().__init__(name, white)
    
    def __str__(self):
        if self.white == True:
            return " "+self.name[1].upper()+" "
        else:
            return " "+self.name[1].lower()+" "
        

    def getPossibleMoves(self,cordsX,cordsY):
        ret = []
        return ret