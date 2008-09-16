import pygame 
from game.gameEntity import GameEntity
from utils.vector2D import Vector2D

class Player(GameEntity):
    
    refToGameWorld  = None
    crosshairPos    = Vector2D(0,0)
    playerId        = 0
    isAiPlayer      = False
    
    def __init__(self, playerId, isAiPlayer = False):
        GameEntity.__init__(self)
        self.playerId   = playerId 
        self.isAiPlayer = isAiPlayer
        self.position   = Vector2D(10.0,10.0)
        self.checkVisibility = False
        
    # Set crosshair position
    def setCrosshairPos(self, pos):
        self.crosshairPos = pos
        
    # set unit movment 
    def setMovment( self, direction, unitSpeed ):
        self.direction = direction
        self.unitSpeed = unitSpeed
        
    # update player
    def update(self, timePassed):
        GameEntity.update( self, timePassed )
        self.refToGameWorld.setViewport( self.position )
        
    def render(self, surface, renderRect):
        
        GameEntity.render( self, surface, self.rect )
        ## Draw crosshair ##
        
        # circle 
        pygame.draw.circle( surface, (255,0,0), self.crosshairPos, 8, 1 )

        # top - > down 
        startpos = ( self.crosshairPos[0], self.crosshairPos[1] - 5 )
        endpos   = ( self.crosshairPos[0], self.crosshairPos[1] + 5 )
        pygame.draw.line( surface, (255,255,255), startpos, endpos, 1 )
        
        # left -> right
        startpos = (self.crosshairPos[0] - 5, self.crosshairPos[1] )
        endpos   = (self.crosshairPos[0] + 5, self.crosshairPos[1] )
        pygame.draw.line( surface, (255,255,255), startpos, endpos, 1 )
        
        