import pygame 
import random
import getopt, sys

from game import network
from pygame.locals import *
from sys import exit
from game.inputManager import InputManager
from game.mainGameScene import MainGameScene
from game.gameEntityManager import GameEntityManager
from game.imageManager import ImageManager
from game.gameEntity import GameEntity
from utils.vector2D import Vector2D
from game.gameWorld import GameWorld

class MainGame(network.Client):
    
    myInputMngr         = None
    myActiveGameScene   = None
    myScreen            = None
    myGameEntityMngr    = None
    myImgMngr           = None
    myBackground        = None
    myGameWorld         = None
    
    def __init__(self):
        self.entities = {}
        network.Client.__init__(self)
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
        self.myActiveGameScene = MainGameScene(self.myGameEntityMngr, self)
        self.myActiveGameScene.refToPlayer.refToGameWorld = self.myGameWorld
        self.myInputMngr.setActiveGameScene( self.myActiveGameScene )
        
        # Hide mouse cursor
        pygame.mouse.set_visible( True )
        
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
                self.exit() 
            else:
                # Delegate to inputManager
                self.myInputMngr.handleInput(events)
    
    # Refresh graphics
    def refreshGraphics(self):
        self.myGameWorld.renderWorld( self.myScreen )
        self.myGameEntityMngr.render( self.myScreen, self.myGameWorld.getViewPortRect() )
        
    # Handle updates like unit-movment e.g
    def handleUpdates(self, timePassed):
        self.myGameEntityMngr.update(timePassed)

    def run(self, server="localhost", port=8800, user='user1', password='pass1'):
        self.clock = pygame.time.Clock()
        if server == None:
            server = "localhost"
        if port == None:
            port = 8800
        if user == None:
            user = 'user1'
        if password == None:
            password = 'pass1'
        self.connect(server, int(port), user, password)
        pass

    def remote_updateEntity(self, entity):
        self.entities[entity.id] = entity
        return "ok"
    def remote_deactivateEntity(self, entity):
        self.entities[entity.id].active = False
        return "ok"
    def remote_activateEntity(self, entity):
        if not self.entities.has_key(entity.id):
            self.entities[entity.id] = entity
        self.entities[entity.id].active = True
        return "ok"
    def mainIteration(self):
        timePassed = self.clock.tick(25) / 100.0 #Time in seconds
        self.handleUpdates( timePassed )
        self.refreshGraphics()
        for entity in self.entities.values():
            if entity.active == True:
                infoSurface = pygame.font.SysFont("arial",16)
                txtSurface = infoSurface.render( "x", True, (255,255,255))
                #print "..",entity.position 
                self.myScreen.blit( txtSurface, entity.position )

        pygame.display.flip()

def usage():
    print "usage:"
    print " -H <host>"
    print " -P <port>"
    print " -u <username>"
    print " -p <password>"
                
# Start maingame
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hH:P:u:p:v")
    except:
        usage()
        exit(2)
    server = None
    port = None
    user = None
    password = None
    for o, a in opts:
        if o == '-H':
            server = a
        if o == '-P':
            port = a
        if o == '-u':
            user = a
        if o == '-p':
            password = a
        if o == '-h':
            usage()
            sys.exit(2)
    mainGame = MainGame()
    mainGame.run(server,port,user,password)               
