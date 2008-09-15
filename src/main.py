import pygame 
import random

from pygame.locals import *
from sys import exit
from game.inputManager import InputManager
from game.mainGameScene import MainGameScene
from game.gameEntityManager import GameEntityManager
from game.imageManager import ImageManager
from game.gameEntity import GameEntity
from utils.vector2D import Vector2D
from game.gameWorld import GameWorld

class MainGame:
    
    myInputMngr         = None
    myActiveGameScene   = None
    myScreen            = None
    myGameEntityMngr    = None
    myImgMngr           = None
    myBackground        = None
    myGameWorld         = None
    
    def __init__(self):
        pygame.init()   
        self.myScreen = pygame.display.set_mode( ( 1024, 768 ), HWSURFACE | DOUBLEBUF, 32 )
        pygame.display.set_caption("Cannon Fodder Reloaded")
        
        # Image Manager and background
        self.myImgMngr = ImageManager()
        self.myImgMngr.loadTerrainTextures()
        
        # GameEntity Manager
        self.myGameEntityMngr = GameEntityManager()
        self.myGameEntityMngr.myImgMngr = self.myImgMngr
        
        self.myGameWorld      = GameWorld()
        self.myGameWorld.myImgMngr = self.myImgMngr
        self.myGameWorld.createNewTerrain( "gras0001.png", (1024,768) )
        
        # Initialize InputManager, GameScene 
        self.myInputMngr = InputManager()
        self.myActiveGameScene = MainGameScene(self.myGameEntityMngr)
        self.myActiveGameScene.refToPlayer.refToGameWorld = self.myGameWorld
        self.myInputMngr.setActiveGameScene( self.myActiveGameScene )
        
        # Hide mouse cursor
        pygame.mouse.set_visible( False )
        
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
       # self.myScreen.blit( self.myBackground, (0,0,1024,768) )
        self.myGameWorld.renderWorld( self.myScreen )
        self.myGameEntityMngr.render( self.myScreen, self.myGameWorld.getViewPortRect() )
        
    # Handle updates like unit-movment e.g
    def handleUpdates(self, timePassed):
        self.myGameEntityMngr.update(timePassed)

    # Main-Game Loop
    def mainLoop(self):
        # Initialize clock
        clock = pygame.time.Clock()
        
        while True:
            timePassed = clock.tick(25) / 1000.0 #Time in seconds          
            # handle events 
            self.handleEvents()
            # Perform unit updates 
            self.handleUpdates( timePassed )
            # Refresh graphics 
            self.refreshGraphics()
            # Flip doublebuffer
            pygame.display.flip()

                
# Start maingame
if __name__ == '__main__':
    mainGame = MainGame()
    mainGame.mainLoop()               
            