import pygame
from pygame.locals import * 
from game.gameScene import GameScene
from utils.vector2D import Vector2D
from game.player import Player

class MainGameScene( GameScene ):
    
    refToGameEntiyMngr  = None
    refToPlayer         = None

    def __init__(self, refToGameEntiyMngr):
        self.refToGameEntiyMngr = refToGameEntiyMngr
        
        self.refToGameEntiyMngr.loadUnit("Clone")
        self.refToPlayer = Player( 0, False )
        self.refToPlayer.name = "Clone"
        
        self.refToGameEntiyMngr.addEntity( self.refToPlayer )
    
    def handleMouseInput(self, mousebutton, mousePos, state = 'PRESSED'):
        if state == 'PRESSED':
            if mousebutton == 1:
                self.refToGameEntiyMngr.loadAndCreateUnit('objects/tree1', Vector2D(mousePos[0],mousePos[1]), Vector2D(0,0), 0)
            elif mousebutton == 3:
                trgtVec     = Vector2D( mousePos[0], mousePos[1] )
                direction   = direction = Vector2D.fromPoints( self.refToPlayer.position, trgtVec )
                direction.normalizeVector()
                self.refToPlayer.setMovment( direction, 20.0 )
        else:
            self.refToPlayer.setMovment( Vector2D( 0,0 ), 0.0 )        

    def handleMouseMovment(self,mousePos):
        if self.refToPlayer is not None:
            self.refToPlayer.setCrosshairPos( mousePos )
    
    def handleKeyInput(self, key, modifier, state = 'PRESSED' ):
        if state == 'PRESSED':
            if key == K_a:
                self.refToPlayer.setMovment( Vector2D(-1, 0), 20.0 )
            elif key == K_d:
                self.refToPlayer.setMovment( Vector2D(1, 0), 20.0 )
            elif key == K_w:
                self.refToPlayer.setMovment( Vector2D(0, -1), 10.0 )
            elif key == K_s:
                self.refToPlayer.setMovment( Vector2D(0, 1), 20.0 )
            elif key == K_RETURN and modifier & KMOD_LALT == KMOD_LALT:
                pygame.display.toggle_fullscreen()
            elif key == K_ESCAPE:
                exit()
        else:
            self.refToPlayer.setMovment( Vector2D(0,0), 10.0 )        