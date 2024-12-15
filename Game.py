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
        return enPesent(piece,row, col)[0]
    
        
    return piece.getPossibleMoves(row, col)



def castling(piece, row, col):
    ret  = piece.getPossibleMoves(row, col)
    castling = []

    if isinstance(piece,King):
        l =True
        r=True
        if not piece.moved:
            if piece.white:
                for num in range(1,8):
                    if r:
                        if col+num<9:

                            add =True

                            if  isinstance(ChessBoard.board[row][col+num],Rook) or  isinstance(ChessBoard.board[row][col+num],ChessBoard.null) :
                                if not isinstance(ChessBoard.board[row][col+num],ChessBoard.null) and not ChessBoard.board[row][col+num].moved:
                            
                                    ChessBoard.movePiece("1","e","1","g")
                                    ChessBoard.movePiece("1","h","1","f")
                                    for piece1 in ChessBoard.pieces:
                                        if ("+", 1, chr(7+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]) or ("e", 1, chr(6+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]):
                                            add = not add
                                            break    


                                    ChessBoard.movePiece("1","f","1","h")
                                    ChessBoard.movePiece("1","g","1","e")

                                    if add: 
                                        ret.append(("c", 1, chr(7+64)))
                                        castling.append(("c", 1, chr(7+64)))

                            else:
                                r =not r



                                

                        else:
                            r = not r

                    if l:
                        if col - num>0:
                            add =True

                            if  isinstance(ChessBoard.board[row][col-num],Rook) or  isinstance(ChessBoard.board[row][col-num],ChessBoard.null) :
                                if not isinstance(ChessBoard.board[row][col-num],ChessBoard.null) and not ChessBoard.board[row][col-num].moved:

                                    ChessBoard.movePiece("1","e","1","c")
                                    ChessBoard.movePiece("1","a","1","d")
                                    for piece1 in ChessBoard.pieces:
                                        if ("+", 1, chr(3+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]) or ("e", 1, chr(4+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]):
                                            add = not add
                                            break    
                                    
                                    ChessBoard.movePiece("1","c","1","e")
                                    ChessBoard.movePiece("1","d","1","a")

                                    if add:
                                        ret.append(("c", 1, chr(3+64)))
                                        castling.append(("c", 1, chr(3+64)))

                            else:
                                l = not l       
                        else:
                            l = not l
                
            else:
                for num in range(1,8):
                    if r:
                        if col+num<9:

                            add =True
                            
                            if  isinstance(ChessBoard.board[row][col+num],Rook) or  isinstance(ChessBoard.board[row][col+num],ChessBoard.null) :
                                if not isinstance(ChessBoard.board[row][col+num],ChessBoard.null) and not ChessBoard.board[row][col+num].moved:

                                    ChessBoard.movePiece("8","e","8","g")
                                    ChessBoard.movePiece("8","h","8","f")
                                    for piece1 in ChessBoard.pieces:
                                        if ("+", 8, chr(7+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]) or ("e", 8, chr(6+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]):
                                            add = not add
                                            continue    


                                    ChessBoard.movePiece("8","g","8","e")
                                    ChessBoard.movePiece("8","f","8","h")


                                    if add:
                                        ret.append(("c", 8, chr(7+64)))
                                        castling.append(("c", 8, chr(7+64)))
                            else:
                                r = not r
                                

                        else:
                            r = not r

                    if l:
                        if col - num>0:
                            add =True
                            if  isinstance(ChessBoard.board[row][col-num],Rook) or  isinstance(ChessBoard.board[row][col-num],ChessBoard.null) :
                                if not isinstance(ChessBoard.board[row][col-num],ChessBoard.null) and not ChessBoard.board[row][col-num].moved:

                                    ChessBoard.movePiece("8","e","8","c")
                                    ChessBoard.movePiece("8","a","8","d")
                                    for piece1 in ChessBoard.pieces:
                                        if ("+", 8, chr(3+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]) or ("e", 8, chr(4+64)) in piece1[0].getPossibleMoves(piece1[1][0],piece1[1][1]):
                                            add = not add
                                            break    

                                    ChessBoard.movePiece("8","c","8","e")
                                    ChessBoard.movePiece("8","d","8","a")

                                    if add:
                                        ret.append(("c", 8, chr(3+64)))
                                        castling.append(("c", 8, chr(3+64)))

                            else:
                                l = not l


                        else:
                            l=not l


        return [ret,castling]

     



def enPesent(piece,row, col):
    enPesent = []
    ret = piece.getPossibleMoves(row, col)
    global curentMove

    if piece.counter == 0:
        piece.counter =curentMove

    
    if col -1 >0 and isinstance(ChessBoard.board[row][col-1] ,Pawn):
        if piece.white:
            if not(ChessBoard.board[row][col-1].white==piece.white) and ChessBoard.board[row][col-1].counter == curentMove-1 :
                ret.append(("e",(row+1),chr(col+64-1)))
                enPesent.append(("e",(row+1),chr(col+64-1)))
        else:
            if not(ChessBoard.board[row][col-1].white==piece.white) and ChessBoard.board[row][col-1].counter == curentMove-1 :
                ret.append(("e",(row-1),chr(col+64-1)))
                enPesent.append(("e",(row-1),chr(col+64-1)))

    if col +1 <9 and isinstance(ChessBoard.board[row][col+1] ,Pawn):
        if piece.white:
            if not(ChessBoard.board[row][col+1].white==piece.white) and ChessBoard.board[row][col+1].counter == curentMove-1 :
                ret.append(("e",(row+1),chr(col+64+1)))
                enPesent.append(("e",(row+1),chr(col+64+1)))
        else:
            if not(ChessBoard.board[row][col+1].white==piece.white) and ChessBoard.board[row][col+1].counter == curentMove-1 :
                ret.append(("e",(row-1),chr(col+64+1)))
                enPesent.append(("e",(row-1),chr(col+64+1)))


    
    return [ret,enPesent]


def kingMoves(piece,cords,row, col):
    possibleKingMoves = piece.getPossibleMoves(row, col)
    new_possibleKingMoves = []
    for move in possibleKingMoves:
        new_possibleKingMoves.append(move)

        
    lMove = [cords[0],cords[1]]
    board = [[" " for _ in range(9)] for _ in range(9)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j]=ChessBoard.board[i][j]


    for possibleMove in possibleKingMoves:

        ChessBoard.movePiece(lMove[0],lMove[1],possibleMove[1],possibleMove[2])


        for piece1 in ChessBoard.pieces:


            if piece1[0].white == piece.white:
                continue
            
            if possibleMove not in new_possibleKingMoves:
                continue




            if ("+",(possibleMove[1]),(possibleMove[2])) in piece1[0].getPossibleMoves(*piece1[1]):
                new_possibleKingMoves.remove(possibleMove)

            

        ChessBoard.movePiece(possibleMove[1],possibleMove[2],lMove[0],lMove[1])
        ChessBoard.setBoardToAnExistingBoard(board)
        
    for cassMove in castling(piece, row, col)[0]:
        if cassMove not in possibleKingMoves:
            new_possibleKingMoves.append(cassMove)

    
    return new_possibleKingMoves

def move(oldCords,newCords):

    global curentMove
    

    canMove = True

    if  not isinstance(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64], ChessPiece):  # Check if it's a chess piece
        canMove=not canMove
        print(f"There is not a chess piece in {oldCords[0]}{oldCords[1]}")

    for piece in ChessBoard.pieces:
        
        if not(piece[1][0] ==int(oldCords[0]) and chr(piece[1][1]+64) ==oldCords[1].upper()):
            continue
        

            
        
        if  not((("", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)])) or 
            (("e", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)])) or 
            (("c", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)])) or 
            (("+", int(newCords[0]), newCords[1].upper()) in showMovesFromSpecificPlace([piece[1][0],chr(piece[1][1]+64)]))):            
                print("Not possible move")
                canMove=not canMove
                break
        
        piece[1][0] =int(newCords[0])
        piece[1][1] = ord(newCords[1].upper())-64

    if canMove: 

        if isinstance(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64] ,Pawn):
            if ("e",int(newCords[0]),newCords[1].upper()) in enPesent(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64],int(oldCords[0]),ord(oldCords[1].upper())-64)[1]:
                print(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64])
                if ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64].white:
                    ChessBoard.deleteThePiece(((int(newCords[0])-1),newCords[1]))
                else:
                    ChessBoard.deleteThePiece((newCords[0]+1,newCords[1]))
        elif isinstance(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64],Rook):
            ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64].moved =True
        elif isinstance(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64] ,King): 
            if ("c",int(oldCords[0]),chr(ord(oldCords[1].upper())+2)) in castling(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64],int(oldCords[0]),ord(oldCords[1].upper())-64)[1]:
                ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64].moved =True
                ChessBoard.board[int(oldCords[0])][8].moved =True 
                ChessBoard.movePiece(oldCords[0].upper(),"h",oldCords[0].upper(),"f")    
            elif ("c",int(oldCords[0]),chr(ord(oldCords[1].upper())-2)) in castling(ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64],int(oldCords[0]),ord(oldCords[1].upper())-64)[1]:
                ChessBoard.board[int(oldCords[0])][ord(oldCords[1].upper())-64].moved =True
                ChessBoard.board[int(oldCords[0])][1].moved =True
                ChessBoard.movePiece(oldCords[0].upper(),"a",oldCords[0].upper(),"d")

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





def playGame():
    setBoard()
    won=True   
    white =True
    t=True
    while t :
        won =True
        if white:
            print("White turn")
            
        else:
            print("Black turn")
            
        print(ChessBoard())
        first_choice = input("Where do you want to go from?")
        second_choice = input("Where do you to go ?")
        for piece in ChessBoard.pieces:
            if not(piece[1][0] ==int(first_choice[0]) and chr(piece[1][1]+64) ==first_choice[1].upper()):
                continue

            if not piece[0].white == white:
                print("You moved the wrong piece color")
                break

            white = not white
            move(first_choice,second_choice)

        for piece in ChessBoard.pieces:
            if not(piece[0].white ==white):
                if not(piece[0].getPossibleMoves(piece[1][0],piece[1][1]) == []):
                    won = False

        if won:
            if white:
                print("White won")
            else:
                print("Black won")
            break

                    

        
        
