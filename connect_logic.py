from connect_error import ConnectError
from board import Board

class ConnectLogic():
    PLAYER_Y = 1
    PLAYER_R = 2
    
    def __init__(self, b_row, b_col, **kwarg) -> None:
        print("ConnectLogic init")
        self.ROWS_CNT = b_row
        self.COLUMNS_CNT = b_col
        self.game_board = Board(self.ROWS_CNT, self.COLUMNS_CNT)


    def checkField(self, row, col):
        return self.game_board.getValue(row, col)

    def setField(self, row, col, player):
        color = None
        if player == self.PLAYER_Y: color = Board.YELLOW_P
        elif player == self.PLAYER_R: color = Board.RED_P
        else: 
            raise ConnectError(f"Invalid player value: {player}")
        
        return self.game_board.setValue(row, col, color)