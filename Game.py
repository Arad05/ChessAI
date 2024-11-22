from ChessBoard import ChessBoard
from Pawn import Pawn


def setBoard():
    ChessBoard.setBoard()
    # Put the white pawns
    for i in range(1, len(ChessBoard.board[2])):
        ChessBoard.putThePieceDown(Pawn("pawn", True), [2, i])
    # Put the black pawns
    for i in range(1, len(ChessBoard.board[7])):
        ChessBoard.putThePieceDown(Pawn("pawn", False), [7, i])

setBoard()

print(ChessBoard())


def playGame():
    t=True
    while t :
        print(ChessBoard())
        choice = input("What do you want to do?")
        pass
