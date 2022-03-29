from multiprocessing import Event
import pygame
from typing import Tuple


class Game:
    def __init__(self, window_name:str="I'm just playin'", size:Tuple[int,int] = (900, 600), **kwarg) -> None:
        print("Game init")
        self.SIZE = size
        self.__run = False
        self.window_name = window_name

    def init_pygame(self):
        pygame.init()
        self.game_screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption(self.window_name)
    
    def getScreen(self):
        return self.game_screen

    def __initNewGame(self):
        self.__run = True

    def __endGame(self):
        pass
        
    
    def starGame(self):
        self.__initNewGame()
        #setup main loop
        while self.__run == True:
            for event in pygame.event.get():
                self.handleEvent(event)
            
            

        pygame.quit()

    
    def draw(self):
        pygame.display.update()
    


    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.onQuit(event)
        else:
            self.onOther(event)
            
    ###game events
    
    def onQuit(self, event):
        print("onQuit")
        self.__run = False
        
    def onOther(self, event:Event):
        e_name = pygame.event.event_name(event.type)
        #print(f"unhandled event: {e_name}")

if __name__ == "__main__":
    pass