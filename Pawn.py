from ChessPiece import ChessPiece
from ChessBoard import ChessBoard

class Pawn(ChessPiece):
    
    def __init__(self,name,white):
        super().__init__(name, white)
        self.counter =0
    
    def __str__(self):
        return super().__str__()
        

    def getPossibleMoves(self,cordsX,cordsY):

        ret = []

        # Moves for white

        if self.white: 
            
            if str(ChessBoard.board[cordsX+1][cordsY]) == str(ChessBoard.null()):
                ret.append(((cordsX+1),chr(cordsY+64)))
                # If first move
                if self.counter ==0:
                    if str(ChessBoard.board[cordsX+2][cordsY]) == str(ChessBoard.null()):
                        ret.append(((cordsX+2),chr(cordsY+64)))
            #
            #  Eating right
            if not(str(ChessBoard.board[cordsX+1][cordsY+1]) == str(ChessBoard.null())):
                if ChessBoard.board[cordsX+1][cordsY+1].white == False:
                    ret.append(((cordsX+1),chr(cordsY+64+1)))
            
            # Eating right
            if not(str(ChessBoard.board[cordsX+1][cordsY-1]) == str(ChessBoard.null())):
                if ChessBoard.board[cordsX+1][cordsY-1].white == False:
                    ret.append(((cordsX+1),chr(cordsY+64-1)))
            # En pesent
 
            # if str(ChessBoard.board[cordsX][cordsY-1]) == str(Pawn()):
            #     if ChessBoard.board[cordsX][cordsY-1].white == False:
            #         if ChessBoard.board[cordsX][cordsY-1].count == 1:
            #             ret.append(((cordsX+1),chr(cordsY+64-1)))
                

        # Moves for black
        else:
            if str(ChessBoard.board[cordsX-1][cordsY]) == str(ChessBoard.null()):
                ret.append(((cordsX-1),chr(cordsY+64)))
                # If first move
                if self.counter ==0:
                    if str(ChessBoard.board[cordsX-2][cordsY]) == str(ChessBoard.null()):
                        ret.append(((cordsX-2),chr(cordsY+64)))
            
            #  Eating right
            if not(str(ChessBoard.board[cordsX-1][cordsY+1]) == str(ChessBoard.null())):
                if ChessBoard.board[cordsX-1][cordsY+1].white == False:
                    ret.append(((cordsX-1),chr(cordsY+64+1)))
            
            # Eating right
            if not(str(ChessBoard.board[cordsX-1][cordsY-1]) == str(ChessBoard.null())):
                if ChessBoard.board[cordsX-1][cordsY-1].white == False:
                    ret.append(((cordsX-1),chr(cordsY+64-1)))
                    
        return ret