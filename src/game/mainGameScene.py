import pygame
from pygame.locals import * 
from game.gameScene import GameScene
from utils.vector2D import Vector2D
from game.player import Player

class MainGameScene( GameScene ):
    
    refToGameEntiyMngr  = None
    refToPlayer         = None
    mouseButtonPressed  = False

    def __init__(self, refToGameEntiyMngr):
        self.refToGameEntiyMngr = refToGameEntiyMngr
        
        self.refToGameEntiyMngr.loadUnit("Clone")
        self.refToPlayer = Player( 0, False )
        self.refToPlayer.name = "Clone"
        
        self.refToGameEntiyMngr.addEntity( self.refToPlayer )
    
    def handleMouseInput(self, mousebutton, mousePos, state = 'PRESSED'):
        if state == 'PRESSED':
            if mousebutton == 1:
                #self.refToGameEntiyMngr.loadAndCreateUnit('objects/tree1', Vector2D(mousePos[0],mousePos[1]), Vector2D(0,0), 0)
                self.refToGameEntiyMngr.createExplosion('explosions/bigDirty', Vector2D(mousePos[0],mousePos[1]), 0.2 )
            elif mousebutton == 3:  
                self.mouseButtonPressed = True
        else:
            if mousebutton == 3:
                self.mouseButtonPressed = False
                self.refToPlayer.setMovment( Vector2D( 0,0 ), 0.0 )

    def handleMouseMovment(self,mousePos):
        if self.refToPlayer is not None:
            self.refToPlayer.setCrosshairPos( mousePos )
            
            if self.mouseButtonPressed is True:
                trgtVec     = Vector2D( mousePos[0], mousePos[1] )
                direction   = direction = Vector2D.fromPoints( self.refToPlayer.position, trgtVec )
                direction.normalizeVector()
                self.refToPlayer.setMovment( direction, 20.0 )
    
    def handleKeyInput(self, key, modifier, state = 'PRESSED' ):
        pass 