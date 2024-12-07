from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Pawn(ChessPiece):
    
    def __init__(self,name,white):
        super().__init__(name, white)
        self.counter =0
    
    def __str__(self):
        return super().__str__()
        
    def transform(self,Upgrade,cords):
        ChessBoard.putThePieceDown(Upgrade,[cords[0],ord(cords[1].upper()) - 64])

    def getPossibleMoves(self,cordsX,cordsY):

        ret = []

        # Moves for white

        if self.white: 
            
            if str(ChessBoard.board[cordsX+1][cordsY]) == str(ChessBoard.null()):
                ret.append(("",(cordsX+1),chr(cordsY+64)))
                # If first move
                if self.counter ==0:
                    if str(ChessBoard.board[cordsX+2][cordsY]) == str(ChessBoard.null()):
                        ret.append(("",(cordsX+2),chr(cordsY+64)))
            #
            #  Eating right
            if(0<cordsX+1<9 and 0<cordsY+1<9):
                if not(str(ChessBoard.board[cordsX+1][cordsY+1]) == str(ChessBoard.null())):
                    if ChessBoard.board[cordsX+1][cordsY+1].white == False:
                        if isinstance(ChessBoard.board[cordsX+1][cordsY+1], King):
                            ret.append(("+",(cordsX+1),chr(cordsY+64+1)))
                        else:
                            ret.append(("e",(cordsX+1),chr(cordsY+64+1)))
            
            # Eating right
            if(0<cordsX+1<9 and 0<cordsY-1<9):
                if not(str(ChessBoard.board[cordsX+1][cordsY-1]) == str(ChessBoard.null())):
                    if ChessBoard.board[cordsX+1][cordsY-1].white == False:
                        if isinstance(ChessBoard.board[cordsX-1][cordsY+1], King):
                            ret.append(("+",(cordsX+1),chr(cordsY+64-1)))
                        else:
                            ret.append(("e",(cordsX+1),chr(cordsY+64-1)))
            # En pesent
 
            # if str(ChessBoard.board[cordsX][cordsY-1]) == str(Pawn()):
            #     if ChessBoard.board[cordsX][cordsY-1].white == False:
            #         if ChessBoard.board[cordsX][cordsY-1].count == 1:
            #             ret.append(((cordsX+1),chr(cordsY+64-1)))
                

        # Moves for black
        else:
            if str(ChessBoard.board[cordsX-1][cordsY]) == str(ChessBoard.null()):
                ret.append(("",(cordsX-1),chr(cordsY+64)))
                # If first move
                if self.counter ==0:
                    if str(ChessBoard.board[cordsX-2][cordsY]) == str(ChessBoard.null()):
                        ret.append(("",(cordsX-2),chr(cordsY+64)))
            
            #  Eating right
            if(0<cordsX-1<9 and 0<cordsY+1<9):
                if not(str(ChessBoard.board[cordsX-1][cordsY+1]) == str(ChessBoard.null())):
                    if ChessBoard.board[cordsX-1][cordsY+1].white == True:
                        if isinstance(ChessBoard.board[cordsX-1][cordsY+1], King):
                            ret.append(("+",(cordsX-1),chr(cordsY+64+1)))
                        else:
                            ret.append(("e",(cordsX-1),chr(cordsY+64+1)))
            
            # Eating right
            if(0<cordsX-1<9 and 0<cordsY-1<9):
                if not(str(ChessBoard.board[cordsX-1][cordsY-1]) == str(ChessBoard.null())):
                    if ChessBoard.board[cordsX-1][cordsY-1].white == True:
                        if isinstance(ChessBoard.board[cordsX-1][cordsY-1], King):
                            ret.append(("+",(cordsX-1),chr(cordsY+64-1)))
                        else:
                            ret.append(("e",(cordsX-1),chr(cordsY+64-1)))
                    
        return ret