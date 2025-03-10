from Pawn import Pawn
from ChessBoard import ChessBoard

pawn = Pawn("pawn",True)
print(pawn)

# Create and prepare the chessboard

ChessBoard.setBoard()
ChessBoard.board[5][5]= "k "
# ChessBoard.board[3][4]="q "
print(ChessBoard())
# ChessBoard.movePiece(5,"e", 3, "D")
# print(ChessBoard.display())
# ChessBoard.movePiece( 3, "D",5,"C")
# print(ChessBoard.display())
