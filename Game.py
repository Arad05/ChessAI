from ChessBoard import ChessBoard
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from ChessPiece import ChessPiece


curentMove = 0

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

    

     
def showWhoCanGetToASpecifcPlace(cords):
    ret = []
    row = int(cords[0])  # Convert the row number from string to integer
    col = ord(cords[1].upper()) - 64  # Convert column letter to index
    
    if not(0<row<9 and 0<col<9):
        return ret
    
    for piece in ChessBoard.pieces:

        print(piece[0],piece[0].getPossibleMoves(piece[1][0],piece[1][1]))
        if str(ChessBoard.board[row][col]) == str(ChessBoard.null()) :
            print(piece[0].getPossibleMoves(piece[1][0],piece[1][1]))
            if ("", int(row), chr(col+64)) in piece[0].getPossibleMoves(piece[1][0],piece[1][1]):
                ret.append((str(piece[0]),piece[1]))

        elif str(ChessBoard.board[row][col]) == str(King("king", not(piece[0].white))) and ("+", int(row), chr(col+64)) in piece[0].getPossibleMoves(*piece[1]):
            ret.append((str(piece[0]),piece[1]))
        elif ("e", int(row), chr(col+64)) in piece[0].getPossibleMoves(piece[1][0],piece[1][1]):
        
            ret.append((str(piece[0]),piece[1]))
    return ret            

def normalPieceMoves(piece,row, col):
    for piece1 in ChessBoard.pieces:

        if piece1[0].white == piece.white:
            continue

        for move in piece1[0].getPossibleMoves(*piece1[1]):
            
            if not(move[0] == "+"):
                continue

            return []
    if isinstance(piece, Pawn):
        return pawnMoves(piece,row, col)
        
    return piece.getPossibleMoves(row, col)


#need fixing
def pawnMoves(piece,row, col):
    ret = piece.getPossibleMoves(row, col)
    global curentMove

    if piece.counter == 0:
        piece.counter =curentMove

    
    if isinstance(ChessBoard.board[row][col-1] ,Pawn):
        if piece.white:
            if col -1 >0:
                if not(ChessBoard.board[row][col-1].white==piece.white):
                    if ChessBoard.board[row][col-1].counter == curentMove-1:
                        ret.append(("e",(row+1),chr(col+64-1)))
        else:
            if col -1 >0:
                if not(ChessBoard.board[row][col-1].white==piece.white):
                    if ChessBoard.board[row][col-1].counter == curentMove-1:
                        ret.append(("e",(row-1),chr(col+64-1)))

    if isinstance(ChessBoard.board[row][col+1] ,Pawn):
        if piece.white:
            if col +1 <9:
                if not(ChessBoard.board[row][col+1].white==piece.white):
                    if ChessBoard.board[row][col+1].counter == curentMove-1:
                        ret.append(("e",(row+1),chr(col+64+1)))
        else:
            if col +1 <9:
                if not(ChessBoard.board[row][col+1].white==piece.white):
                    if ChessBoard.board[row][col+1].counter == curentMove-1:
                        ret.append(("e",(row-1),chr(col+64+1)))


    
    return ret


def kingMoves(piece,cords,row, col):
    possibleKingMoves = piece.getPossibleMoves(row, col)
    new_possibleKingMoves = []
    for move in possibleKingMoves:
        new_possibleKingMoves.append(move)

        
    lMove = [cords[0],cords[1]]
    board =ChessBoard.board


    for possibleMove in possibleKingMoves:

        ChessBoard.movePiece(lMove[0],lMove[1],possibleMove[1],possibleMove[2])


        for piece1 in ChessBoard.pieces:


            if piece1[0].white == piece.white:
                continue
            
            if possibleMove not in new_possibleKingMoves:
                continue




            if ("+",(possibleMove[1]),(possibleMove[2])) in piece1[0].getPossibleMoves(*piece1[1]):
                new_possibleKingMoves.remove(possibleMove)

            
        lMove = [possibleMove[1],possibleMove[2]]

            
        ChessBoard.board=board

    ChessBoard.movePiece(lMove[0],lMove[1],cords[0],cords[1])
    
    return new_possibleKingMoves

def move(oldCords,newCords):

    global curentMove


    canMove = True

    for piece in ChessBoard.pieces:
        
        if not(piece[1][0] ==int(oldCords[0]) and chr(piece[1][1]+64) ==oldCords[1].upper()):
            continue
            
        if  not((("", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)])) or 
            (("e", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)])) or 
            (("+", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)]))):            
                print("Not possible move")
                canMove=not canMove
                break

        piece[1][0] =int(newCords[0])
        piece[1][1] = ord(newCords[1].upper())-64

    if canMove:    
        ChessBoard.movePiece(oldCords[0],oldCords[1],newCords[0],newCords[1])

    curentMove +=1

def printPiecesPlaces():
    ret =[]
    for piece in ChessBoard.pieces:
        ret.append((str(piece[0]),piece[1]))
    return ret



def showMovesFromSpecificPlace(cords):
    row = int(cords[0])  # Convert the row number from string to integer
    col = ord(cords[1].upper()) - 64  # Convert column letter to index
    
    if not (0 < row < 9 and 0 < col < 9):
        return "Place not in board"
    piece = ChessBoard.board[row][col]

    if not isinstance(piece, ChessPiece):  # Check if it's a chess piece
        return f"There is not a chess piece in {row}{chr(col + 64)}"
    
    if not isinstance(piece, King):
        return normalPieceMoves(piece, row, col)
    
    return kingMoves(piece,cords,row, col)



setBoard()

ChessBoard.putThePieceDown(Pawn("p",True),[5,5])



print(showMovesFromSpecificPlace("5e"))
move("7d","5d")




# ChessBoard.putThePieceDown(King("king",False),[5,7])


print(ChessBoard())

move("5e","6d")


print(ChessBoard())


# def playGame():
#     t=True
#     while t :
#         print(ChessBoard())
#         choice = input("What do you want to do?")
#         pass
