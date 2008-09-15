import pygame
from pygame.locals import *
import random

class GameWorld:
    
    showGrid  = False 
    GRID_SIZE = (25,20)
    myTiles   = []
    gameWorldDimension = (0,0)
    myImgMngr = None
    viewPortRect = Rect(0,0,1024,768)
    
    def toggleGrid(self):
        self.showGrid = not self.showGrid
 
    # Transform rgb-Value to long
    def transformRGBToLong(self, px):
        return px[2] * 65536 + px[1] * 256 + px[0]
    
    def setViewport( self, position ):
        self.viewPortRect.left = position.x
        self.viewPortRect.top  = position.y
        
    # Return viewport
    def getViewPortRect(self):
        return self.viewPortRect
 
    # Load Terrain
    def createNewTerrain(self, textureSet, gameWorldDimension):
        
        self.gameWorldDimension = gameWorldDimension 
        self.myLandscapeSurface = self.myImgMngr.getTextureByName( textureSet ) 
        
    # Render gameworld 
    def renderWorld(self, surface):
        if self.showGrid is True:
            for x in xrange( 0, self.gameWorldDimension[0], self.GRID_SIZE[0] ):
               startpos = (x, 0)
               endpos   = (x, self.gameWorldDimension[1])
               pygame.draw.line( surface, (0,0,0), startpos, endpos, 1)
                
            for y in xrange( 0, self.gameWorldDimension[1], self.GRID_SIZE[1] ):
               startpos = (0, y)
               endpos   = (self.gameWorldDimension[0], y)
               pygame.draw.line( surface, (0,0,0), startpos, endpos, 1)
            
        # Draw tiles 
        for x in xrange(0, surface.get_width(), self.myLandscapeSurface.get_width()):
            for y in xrange(0, surface.get_height(), self.myLandscapeSurface.get_height()):
                surface.blit( self.myLandscapeSurface, (x,y) )
        
        # Draw information
        font = pygame.font.SysFont( "arial", 16 )
        fontSurface = font.render( "Viewport rect @%s"%self.viewPortRect, True, (255,255,255))
        surface.blit( fontSurface, (300,10) )