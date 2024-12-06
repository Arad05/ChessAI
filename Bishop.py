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
        lu =True
        ru =True
        ld = True
        rd =True
        for i in range(1,8):
            if rd:
                if 0<cordsX+i<9 and 0<cordsY+i<9: 
                    if str(ChessBoard.board[cordsX+i][cordsY+i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX+i, chr(cordsY+i+64)))
                    elif not(ChessBoard.board[cordsX+i][cordsY+i].white == self.white):
                        if str(ChessBoard.board[cordsX+i][cordsY+i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX+i, chr(cordsY+i+64)))
                        else:
                            ret.append(("e",cordsX+i, chr(cordsY+i+64)))
                        rd = not rd
                    else:
                        rd = not rd
            if ru:
                if 0<cordsX-i<9 and 0<cordsY+i<9: 
                    if str(ChessBoard.board[cordsX-i][cordsY+i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX-i, chr(cordsY+i+64)))
                    elif not(ChessBoard.board[cordsX-i][cordsY+i].white == self.white):
                        if str(ChessBoard.board[cordsX-i][cordsY+i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX-i, chr(cordsY+i+64)))
                        else:
                            ret.append(("e",cordsX-i, chr(cordsY+i+64)))
                        ru = not ru
                    else:
                        ru = not ru
            if ld:
                if 0<cordsX+i<9 and 0<cordsY-i<9: 
                    if str(ChessBoard.board[cordsX+i][cordsY-i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX+i, chr(cordsY-i+64)))
                    elif not(ChessBoard.board[cordsX+i][cordsY-i].white == self.white):
                        if str(ChessBoard.board[cordsX+i][cordsY-i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX+i, chr(cordsY-i+64)))
                        else:
                            ret.append(("e",cordsX+i, chr(cordsY-i+64)))
                        ld = not ld
                    else:
                        ld = not ld
            if lu:
                if 0<cordsX-i<9 and 0<cordsY-i<9: 
                    if str(ChessBoard.board[cordsX-i][cordsY-i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX-i, chr(cordsY-i+64)))
                    elif not(ChessBoard.board[cordsX-i][cordsY-i].white == self.white):
                        if str(ChessBoard.board[cordsX-i][cordsY-i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX-i, chr(cordsY-i+64)))
                        else:
                            ret.append(("e",cordsX-i, chr(cordsY-i+64)))
                        lu = not lu
                    else:
                        lu = not lu
                    
        return ret