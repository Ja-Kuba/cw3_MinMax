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
    MAX_SERIES_LEN = 4

    def __init__(self, rows:int, columns:int) -> None:
        self.checkSize(rows, columns)
        self.rows = rows
        self.columns = columns
        self.board = self.buildBoard()
    
    def copy(self):
        new_board = Board(self.rows, self.columns)
        new_board.board = self.board.copy()
        return new_board
    
    def checkSize(self, rows, columns):
        if not ((rows >= 4 and columns >= 2) or (rows >= 4 and columns >= 2)):
            raise ConnectError("invalid game dimensions")
            
    
    def buildBoard(self):
        return np.zeros((self.rows, self.columns))
        
    def getBoard(self):
        return self.board
    
    def getValue(self, row:int, col:int)->int:
        return int(self.board[row][col])
    
    def setValue(self, row:int, col:int, color)->int:
        if self.isValidField(row, col):
            self.board[row][col] = color
        else:
            raise ConnectError(f"invalid position: ({row}, {col})")
            
    
    def getNextMoveInColumn(self, c):
        r = self.rows - 1
        while r >= 0:
            if self.board[r][c] == 0:
                return (r, c)
            r-=1
        return None
        
    def isValidField(self, r, c):
        if r < 0 or r >= self.rows: return False
        elif c < 0 or c >= self.columns: return False
        else: return True
            

    def anyMovesLeft(self):
        if (self.board[0] == 0).sum(): return True
        else: return False
    
    def getAllValidMoves(self)->list:
        moves = []
        for c in range(self.columns):
            mv = self.getNextMoveInColumn(c)
            if mv: moves.append(mv)
        
        return moves
            

    
    def buildVectors(self, row, col):
        series = []
        series.append(self.getSeriesVector(row,col,-1, 1))
        series.append(self.getSeriesVector(row,col, 1, 1))
        series.append(self.getSeriesVector(row,col, 0, 1))
        series.append(self.getSeriesVector(row,col, 1, 0))
        
        return series
        
    #not optimal 
    #some break could be added if any series == 4
    def findLongestSeries(self, row, col, r_dir, c_dir, **kwargs):
        vec = self.getSeriesVector(row, col, r_dir, c_dir, **kwargs)
        y_series = []
        r_series = []
        l = len(vec)
        if l >= 4:
            for i in range(l-3):
                y_tmp, r_tmp = self.countSeries(vec[i:i+4])
                if not r_tmp: y_series.append(y_tmp)
                elif not y_tmp: r_series.append(r_tmp)
        return (y_series, r_series)
                 

    
    def countSeries(self, vec):
        y_cnt = 0
        r_cnt = 0
        for v in vec:
            if v == self.YELLOW_P:
                y_cnt+=1
            elif v == self.RED_P:
                r_cnt+=1
        return y_cnt, r_cnt

    
    # x_dir = [-1 | 0 | 1]
    # y_dir = [-1 | 0 | 1]
    # / diagonal  -1,1
    # \ diagonal   1,1
    # - horizontal 0,1
    # | vertical   1,0
    def getSeriesVector(self,row, col, r_dir:int, c_dir:int, max_off:int = 3):
        vec = []
        
        for off in range(-max_off, max_off+1):
            r = row + off * r_dir
            c = col + off * c_dir
            if self.isValidField(r,c):
                vec.append(self.getValue(r,c))

        return vec
            
        
        
        
        
    
    
    
    if __name__ == "__main__":    
        def a():
            return (1, 1)


        
    
        
    
    