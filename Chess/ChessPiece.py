from abc import ABC, abstractmethod

class ChessPiece(ABC):
    
    @abstractmethod
    def __init__(self,name,white):
        self.name =name
        self.white = white
    
    @abstractmethod
    def __str__(self):
        if self.white == True:
            return " "+self.name[0].upper()+" "
        else:
            return " "+self.name[0].lower()+" "


    @abstractmethod
    def getPossibleMoves(self):
        pass