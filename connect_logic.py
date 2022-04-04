from numpy import true_divide
from connect_error import ConnectError
from board import Board
from random import randrange

class ConnectLogic():
    PLAYER_Y = 1
    PLAYER_R = 2
    
    def __init__(self, b_row, b_col, **kwarg) -> None:
        print("ConnectLogic init")
        self.ROWS_CNT = b_row
        self.COLUMNS_CNT = b_col
        self.game_board = Board(self.ROWS_CNT, self.COLUMNS_CNT)
        self.currentPlayer = self.PLAYER_Y 
        self.initMinMax(**kwarg)        
    
    def switchPlayer(self):
        self.currentPlayer = self.switch_player(self.currentPlayer)
    
    
    def switch_player(self, player):
        new_player = self.PLAYER_R if player == self.PLAYER_Y else self.PLAYER_Y
        return new_player
        
    def makeMove(self, r, c):
        self.setField(r, c, self.currentPlayer, self.game_board)      
        self.switchPlayer()
    
       
    
    def setField(self, row, col, player, board):
        color = None
        if player == self.PLAYER_Y: color = Board.YELLOW_P
        elif player == self.PLAYER_R: color = Board.RED_P
        else: 
            raise ConnectError(f"Invalid player value: {player}")
        
        board.setValue(row, col, color)
    
    def checkField(self, row, col):
        return self.game_board.getValue(row, col)
    
    
    '''
    minmax methods
    '''
    def initMinMax(self, minmax_depth=4):
        self.MAX_Player = self.PLAYER_Y
        self.MIN_Player = self.PLAYER_R
        self.MINMAX_DEPTH = minmax_depth
    
    
    
    def MinMax(self):
        m = self.findNextMove_minmax(
            depth=self.MINMAX_DEPTH,
            board=self.game_board.copy(),
            player=self.currentPlayer,
            )
        if m[1]:
            self.makeMove(m[0], m[1])    
            return True

        else: return False
        #m = randrange(len(moves))
    
    
    # return (score:int, move|None)
    def findNextMove_minmax(self, depth, board, player, tree=None)->tuple:
        scores = []
        if depth > 0:
            moves = self.game_board.getAllValidMoves()
            if len(moves) > 0:
        else:
            return best_score

    
    
    
    def scoreMove(self, row, col):
        pass