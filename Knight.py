from ChessPiece import ChessPiece
from ChessBoard import ChessBoard
from King import King

class Knight(ChessPiece):

    def __init__(self,name,white):
        super().__init__(name, white)
    
    def __str__(self):
        if self.white == True:
            return " "+self.name[1].upper()+" "
        else:
            return " "+self.name[1].lower()+" "
        

    def getPossibleMoves(self, cordsX, cordsY):
        ret = []
        
        # Moves for white
        if self.white: 
            moves = [
                (-2, -1), (-2, 1), 
                (-1, -2), (-1, 2),
                (1, -2), (1, 2),
                (2, -1), (2, 1)
            ]
        else:
            moves = [
                (2, -1), (2, 1), 
                (1, -2), (1, 2),
                (-1, -2), (-1, 2),
                (-2, -1), (-2, 1)
            ]
        
        for dx, dy in moves:
            new_x, new_y = cordsX + dx, cordsY + dy
            
            # Check if move is within board boundaries
            if 0 < new_x < 9 and 0 < new_y < 9:
                # Check if square is empty
                if str(ChessBoard.board[new_x][new_y]) == str(ChessBoard.null()):
                    ret.append(("", new_x, new_y))
                else:
                    if not(ChessBoard.board[new_x][new_y].white == self.white):
                        if str(ChessBoard.board[new_x][new_y]) == str(King("king",False)) or str(ChessBoard.board[new_x][new_y]) == str(King("king",True)):
                            ret.append(("+", new_x, new_y))
                        else:
                            ret.append(("e", new_x, new_y))

        return ret