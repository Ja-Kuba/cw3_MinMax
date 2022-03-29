from re import S
from game import *
from connect_logic import ConnectLogic, Board
from connect_error import ConnectError

BLUE_COLOR = (0, 127, 166)
BLACK_COLOR = (0,0,0)
RED_COLOR = (194, 21, 21)
YELLOW_COLOR = (242, 205, 19)
EMPTY_COLOR = (33, 33, 33)


class Connect(ConnectLogic, Game):
    '''
    size - disc size in [px]
    b_row - board rows count
    b_col - board columns count
    '''
    def __init__(self,b_row:int=6, b_col:int=7, size:int = 100, **kwarg) -> None:
        super().__init__(b_row, b_col, **kwarg)
        super(ConnectLogic, self).__init__(size=(b_col*size, b_row*size), 
                                           window_name="connect4", **kwarg) 
        self.init_pygame()
        self.DISC_SIZE = size
        

        print(self.game_board.getBoard()) 
        self.draw_board()
        self.setField(0,0, 1)
        self.setField(5,6, 2)
        self.setField(6,6, 1)
        print(self.game_board.getBoard()) 
        self.draw_board()

    def draw_board(self):
        for c in range(self.COLUMNS_CNT):
            for r in range(self.ROWS_CNT):
                f_color = self.getFieldColor(r, c)
                x = c*self.DISC_SIZE
                y = r*self.DISC_SIZE
                s = self.DISC_SIZE
                self.drawField(x, y, s, f_color)
        self.draw()


    def drawField(self, x, y, s, color):
                pygame.draw.rect(
                    self.getScreen(),
                    BLUE_COLOR,  
                    (x, y, s, s),                    
                )
                pygame.draw.circle(
                    self.getScreen(),
                    EMPTY_COLOR,
                    (   
                        int(x + s/2),
                        int(y + s/2)
                    ), 
                    int(s/2 - 10)
                )
                pygame.draw.circle(
                    self.getScreen(),
                    color,
                    (   
                        int(x + s/2),
                        int(y + s/2)
                    ), 
                    int(s/2 - 12)
                )
        
        

    def getFieldColor(self, row, col):
        f = self.checkField(row, col)
        if f == Board.EMPTY: return EMPTY_COLOR
        elif f == Board.RED_P: return RED_COLOR
        elif f == Board.YELLOW_P: return YELLOW_COLOR
        else:
            raise ConnectError(f"Invalid field value: {f}")

    def draw(self):
        super().draw()
        
        


if __name__ == "__main__":
    g = Connect(b_row=7, b_col=7, size=80)
    g.starGame()