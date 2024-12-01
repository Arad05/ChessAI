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


        for up in range(8):
            new_y= cordsY+up
            if  0 < new_y < 9:
                if str(ChessBoard.board[cordsX][new_y]) == str(ChessBoard.null()):
                    ret.append(("", cordsX, chr(new_y+64)))
                elif not(ChessBoard.board[cordsX][new_y].white == self.white):
                    if str(ChessBoard.board[cordsX][new_y]) == str(King("king",False)) or str(ChessBoard.board[cordsX][new_y]) == str(King("king",True)):
                        ret.append(("+", cordsX, chr(new_y+64)))
                        break
                    else:
                        ret.append(("e", cordsX, chr(new_y+64)))
                        break

        for down in range(8):
            new_y= cordsY-down
            if  0 < new_y < 9:
                if str(ChessBoard.board[cordsX][new_y]) == str(ChessBoard.null()):
                    ret.append(("", cordsX, chr(new_y+64)))
                elif not(ChessBoard.board[cordsX][new_y].white == self.white):
                    if str(ChessBoard.board[cordsX][new_y]) == str(King("king",False)) or str(ChessBoard.board[cordsX][new_y]) == str(King("king",True)):
                        ret.append(("+", cordsX, chr(new_y+64)))
                        break
                    else:
                        ret.append(("e", cordsX, chr(new_y+64)))
                        break

        for add in range(8):
            new_x= cordsY+add
            if  0 < new_x < 9:
                if str(ChessBoard.board[new_x][cordsY]) == str(ChessBoard.null()):
                    ret.append(("", new_x, chr(cordsY+64)))
                elif not(ChessBoard.board[new_x][cordsY].white == self.white):
                    if str(ChessBoard.board[new_x][cordsY]) == str(King("king",False)) or str(ChessBoard.board[new_x][cordsY]) == str(King("king",True)):
                        ret.append(("+", new_x, chr(cordsY+64)))
                        break
                    else:
                        ret.append(("e", new_x, chr(cordsY+64)))
                        break

        for down in range(8):
            new_x= cordsY-down
            if  0 < new_x < 9:
                if str(ChessBoard.board[new_x][cordsY]) == str(ChessBoard.null()):
                    ret.append(("", new_x, chr(cordsY+64)))
                elif not(ChessBoard.board[new_x][cordsY].white == self.white):
                    if str(ChessBoard.board[new_x][cordsY]) == str(King("king",False)) or str(ChessBoard.board[new_x][cordsY]) == str(King("king",True)):
                        ret.append(("+", new_x, chr(cordsY+64)))
                        break
                    else:
                        ret.append(("e", new_x, chr(cordsY+64)))
                        break

        return ret