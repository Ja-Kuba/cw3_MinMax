from connect_error import ConnectError
import numpy as np

'''
    0        col       6
0 [[2. 0. 0. 0. 0. 0. 0.]  
   [0. 0. 0. 0. 0. 0. 0.]
r  [0. 0. 0. 0. 0. 0. 0.]
o  [0. 0. 0. 0. 0. 0. 0.]
w  [0. 0. 0. 0. 0. 0. 0.]
   [0. 0. 0. 0. 0. 0. 0.]
6  [0. 0. 0. 0. 0. 0. 1.]] 

'''
class Board:
    RED_P = 1 
    YELLOW_P = 2 
    EMPTY = 0

    def __init__(self, rows:int, columns:int) -> None:
        self.checkSize(rows, columns)
        self.rows = rows
        self.columns = columns
        self.board = self.buildBoard()
    
    def checkSize(self, rows, columns):
        if not ((rows >= 4 and columns >= 2) or (rows >= 4 and columns >= 2)):
            raise ConnectError("invalid game dimensions")
            
    
    def buildBoard(self):
        return np.zeros((self.rows, self.columns))
        
    def getBoard(self):
        return self.board
    
    def getValue(self, row:int, col:int)->int:
        return self.board[row][col]
    
    def setValue(self, row:int, col:int, color)->int:
        self.board[row][col] = color