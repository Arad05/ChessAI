from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Bishop(ChessPiece):

    def __init__(self,name,white):
        super().__init__(name, white)
    
    def __str__(self):
        return super().__str__()
        

    def getPossibleMoves(self,cordsX,cordsY):
        ret = []
        for i in range(1,8):
            if str(ChessBoard.board[cordsX+i][cordsY+i]) == str(ChessBoard.null()):
                ret.append(("", cordsX+i, chr(cordsY+i+64)))
            elif not(ChessBoard.board[cordsX+i][cordsY+i].white == self.white):
                if str(ChessBoard.board[cordsX+i][cordsY+i]) == str(King(not(self.white))):
                    ret.append(("e",cordsX+i, chr(cordsY+i+64)))
                    
        return ret