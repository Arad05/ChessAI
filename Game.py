from ChessBoard import ChessBoard
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King



def setBoard():
    ChessBoard.makeBoard()
    # Put the white pawns
    for i in range(1, len(ChessBoard.board[2])):
        ChessBoard.putThePieceDown(Pawn("pawn", True), [2, i])
    # Put the black pawns
    for i in range(1, len(ChessBoard.board[7])):
        ChessBoard.putThePieceDown(Pawn("pawn", False), [7, i])

    # Put the white knight's
    ChessBoard.putThePieceDown(Knight("knight",True),[1,7])
    ChessBoard.putThePieceDown(Knight("knight",True),[1,2])
    # Put the black knight's
    ChessBoard.putThePieceDown(Knight("knight",False),[8,7])
    ChessBoard.putThePieceDown(Knight("knight",False),[8,2])

    # Put the white Bishp's
    ChessBoard.putThePieceDown(Bishop("bishop",True),[1,6])
    ChessBoard.putThePieceDown(Bishop("bishop",True),[1,3])
    # Put the black Bishp's
    ChessBoard.putThePieceDown(Bishop("bishop",False),[8,6])
    ChessBoard.putThePieceDown(Bishop("bishop",False),[8,3])

    # Put the white Rook's
    ChessBoard.putThePieceDown(Rook("rook",True),[1,1])
    ChessBoard.putThePieceDown(Rook("rook",True),[1,8])
    # Put the black Rook's
    ChessBoard.putThePieceDown(Rook("rook",False),[8,1])
    ChessBoard.putThePieceDown(Rook("rook",False),[8,8])

    # Put the white queen
    ChessBoard.putThePieceDown(Queen("queen",True),[1,4])
    # Put the black queen
    ChessBoard.putThePieceDown(Queen("queen",False),[8,4])

    # Put the white king
    ChessBoard.putThePieceDown(King("king",True),[1,5])
    # Put the black king
    ChessBoard.putThePieceDown(King("king",False),[8,5])
    

def showMovesFromSpecificPlace(cords):
    row = int(cords[0])  # Convert the row number from string to integer
    col = ord(cords[1].upper()) - 64  # Convert column letter to index
    return ChessBoard.board[row][col].getPossibleMoves(row,col)
     

# setBoard()
ChessBoard.makeBoard()
ChessBoard.putThePieceDown(Knight("Knight",False),[5,5])
print(ChessBoard())

# print()
print(showMovesFromSpecificPlace("5e"))
# def playGame():
#     t=True
#     while t :
#         print(ChessBoard())
#         choice = input("What do you want to do?")
#         pass
