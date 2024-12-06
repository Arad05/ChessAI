from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Rook(ChessPiece):

    def __init__(self,name,white):
        super().__init__(name, white)
    
    def __str__(self):
        return super().__str__()
        

    def getPossibleMoves(self,cordsX,cordsY):
        ret = []
        up =True
        down =True
        left = True
        right =True
        for i in range(1,8):
            if right:
                if 0<cordsY+i<9: 
                    if str(ChessBoard.board[cordsX][cordsY+i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY+i+64)))
                    elif not(ChessBoard.board[cordsX][cordsY+i].white == self.white):
                        if str(ChessBoard.board[cordsX][cordsY+i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX, chr(cordsY+i+64)))
                        else:
                            ret.append(("e",cordsX, chr(cordsY+i+64)))
                        right = not right
                    else:
                        right = not right
            if down:
                if 0<cordsX+i<9: 
                    if str(ChessBoard.board[cordsX+i][cordsY]) == str(ChessBoard.null()):
                        ret.append(("", cordsX+i, chr(cordsY+64)))
                    elif not(ChessBoard.board[cordsX+i][cordsY].white == self.white):
                        if str(ChessBoard.board[cordsX+i][cordsY]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX+i, chr(cordsY+64)))
                        else:
                            ret.append(("e",cordsX+i, chr(cordsY+64)))
                        down = not down
                    else:
                        down = not down
            if left:
                if 0<cordsY-i<9: 
                    if str(ChessBoard.board[cordsX][cordsY-i]) == str(ChessBoard.null()):
                        ret.append(("", cordsX, chr(cordsY-i+64)))
                    elif not(ChessBoard.board[cordsX][cordsY-i].white == self.white):
                        if str(ChessBoard.board[cordsX][cordsY-i]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX, chr(cordsY-i+64)))
                        else:
                            ret.append(("e",cordsX, chr(cordsY-i+64)))
                        left = not left
                    else:
                        left = not left
            if up:
                if 0<cordsX-i<9: 
                    if str(ChessBoard.board[cordsX-i][cordsY]) == str(ChessBoard.null()):
                        ret.append(("", cordsX-i, chr(cordsY+64)))
                    elif not(ChessBoard.board[cordsX-i][cordsY].white == self.white):
                        if str(ChessBoard.board[cordsX-i][cordsY]) == str(King("king",not(self.white))):
                            ret.append(("+",cordsX-i, chr(cordsY+64)))
                        else:
                            ret.append(("e",cordsX-i, chr(cordsY+64)))
                        up = not up
                    else:
                        up = not up

        return ret