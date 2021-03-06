from re import S
from game import *
from connect_logic import ConnectLogic, Board
from connect_error import ConnectError
import sys
from time import perf_counter
from anytree.exporter import DotExporter
from graphviz import Source, render

BLUE_COLOR = (0, 127, 166)
BLACK_COLOR = (0,0,0)
RED_COLOR = (194, 21, 21)
YELLOW_COLOR = (242, 205, 19)
EMPTY_COLOR = (33, 33, 33)
TEXT_COLOR = (32, 112, 8)


class Connect(ConnectLogic, Game):
    '''
    size - disc size in [px]
    b_row - board rows count
    b_col - board columns count
    '''
    TEXT_FIELD_SIZE = 30
    def __init__(self,b_row:int=6, b_col:int=7, size:int = 100, play_on_tick= False, **kwarg) -> None:
        super().__init__(b_row, b_col, **kwarg)
        super(ConnectLogic, self).__init__(size=(b_col*size, self.TEXT_FIELD_SIZE+b_row*size ), 
                                           window_name="connect4", **kwarg) 
        self.DISC_SIZE = size
        self.init_pygame()
        self.draw_board()
        self.play = True
        self.play_on_tick = play_on_tick
        self.tree_history =[]
        

    def draw_board(self):
        s = self.DISC_SIZE
        for c in range(self.COLUMNS_CNT):
            for r in range(self.ROWS_CNT):
                f_color = self.getFieldColor(r, c)
                x = c*self.DISC_SIZE
                y = r*self.DISC_SIZE + self.TEXT_FIELD_SIZE
                self.drawField(x, y, s, f_color)
        self.draw()

    def drawTextField(self):
        pygame.draw.rect(
            self.getScreen(),
            EMPTY_COLOR,  
            (0, 0, self.COLUMNS_CNT*self.DISC_SIZE, self.TEXT_FIELD_SIZE),                    
        )
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
        
    def draw_msg(self, msg):
        self.drawTextField()
        text_surface = self.font.render(msg, False, TEXT_COLOR)
        self.game_screen.blit(text_surface, dest=(10,10))

        
    def draw(self):
        super().draw()
        

    def getFieldColor(self, row, col):
        f = self.checkField(row, col)
        if f == Board.EMPTY: return EMPTY_COLOR
        elif f == Board.RED_P: return RED_COLOR
        elif f == Board.YELLOW_P: return YELLOW_COLOR
        else:
            raise ConnectError(f"Invalid field value: {f}")

    
    def getCurrentPlayer_name(self):
        p = self.getCurrentPlayer()
        if p == self.PLAYER_Y: return "YELLOW"
        else: return "RED"

    def saveHistory(self):
        print("save history")
        if len(self.tree_history) > 2:
            self.saveTree(self.tree_history[-1],1)
            self.saveTree(self.tree_history[-2],2)

    def saveTree(self, root, ind):
        DotExporter(root).to_dotfile(f"root_{ind}.dot")
        Source.from_file(f"root_{ind}.dot")
        render('dot', 'png', f"root_{ind}.dot")
        print("tree rendered") 

    

    def checkResult(self, m_type):
        if m_type == self.WINNER_MOVE:
            self.play = False
            msg = f"winner: {self.getCurrentPlayer_name()}!!!!"
        elif m_type == self.DRAW_MOVE:
            self.play = False
            msg = "game draw :("
        else: 
            msg =f"next move: {self.getCurrentPlayer_name()}"
        self.draw_msg(msg)


    def play_minmax(self):
        if self.play:
            t = perf_counter()
            self.checkResult(self.MinMax(self.tree_history))
            print(f"move time: {perf_counter()-t}")
            self.draw_board()
        

          
    def onTick(self, event):
        if self.play_on_tick:
            self.play_minmax()

    def onKeyUp(self, event):
        if event.key == pygame.K_RETURN:
            self.play_minmax()
        elif event.key == pygame.K_SPACE:
            self.saveHistory()
        elif event.key == pygame.K_p:
            print("pause")
            self.play_on_tick = not self.play_on_tick
        pass

if __name__ == "__main__":
    args = sys.argv
    if not len(args) == 4:
        print("invalid args: connect.py b_row b_col depth")
    else:
        b_row = int(args[1] )
        b_col = int(args[2])
        minmax_depth = int(args[3])
        g = Connect(b_row=b_row, b_col=b_col, size=80,play_on_tick=False ,minmax_depth=minmax_depth)
        g.starGame()
    