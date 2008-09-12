import pygame 

from pygame.locals import *
from sys import exit
from game.inputManager import InputManager
from game.mainGameScene import MainGameScene


class MainGame:
    
    myInputMngr = None
    myActiveGameScene = None
    
    def __init__(self):
        pygame.init()   
        screen = pygame.display.set_mode( ( 1024, 768 ), HWSURFACE | DOUBLEBUF, 32 )
        pygame.display.set_caption("Cannon Fodder Reloaded")
        self.myInputMngr = InputManager()
        self.myActiveGameScene = MainGameScene()
        self.myInputMngr.setActiveGameScene( self.myActiveGameScene )

        
    # Handle events
    def handleEvents(self):
        # Handle events 
        events = pygame.event.get()
        # Loop through events
        for eachEvent in events:
            # Read event-type 
            eventType = eachEvent.type
            
            # When quit, exit program 
            if eventType == QUIT:
                # TODO:: Signalize "end" 
                exit()
            else:
                # Delegate to inputManager
                self.myInputMngr.handleInput(events)
    
    # Refresh graphics
    def refreshGraphics(self):
        pass 
    
    # Handle updates like unit-movment e.g
    def handleUpdates(self):
        pass

    # Main-Game Loop
    def mainLoop(self):
        while True:
            # handle events 
            self.handleEvents()
            # Perform unit updates 
            self.handleUpdates()
            # Refresh graphics 
            self.refreshGraphics()
            # Flip doublebuffer
            pygame.display.flip()

                
# Start maingame
if __name__ == '__main__':
    mainGame = MainGame()
    mainGame.mainLoop()               
            