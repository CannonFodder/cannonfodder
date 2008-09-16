import math 
import pygame

from utils.vector2D import Vector2D
from pygame.sprite import Sprite
from pygame.locals import *

class GameEntity(Sprite):
    
    id              = 0
    position        = Vector2D(0.0, 0.0)
    direction       = Vector2D(0.0, 0.0)
    type            = 0
    unitSpeed       = 0.0
    activeWaypointIndex = 0
    activeDirectionIndex = 0
    name            = ""
    wayPoints       = None
    checkVisibility = True
    isAlive         = True
    currentMode     = 'r'
    maxAnimationScenes = 0
    animationMode = 0
    
    
    def __init__(self, position = Vector2D(0.0, 0.0), direction = Vector2D(0.0, 0.0), unitSpeed = 0.0, name = ""):
        pygame.sprite.Sprite.__init__(self)
        self.id     = 0
        self.type   = 0
        self.position   = position
        self.direction  = direction
        self.unitSpeed  = unitSpeed
        self.name       = name 
        self.image      = None
        self.rect       = Rect(0,0,0,0)
        
        self.infoSurface = pygame.font.SysFont("arial",16)
        
    # Set image 
    def setImage(self, img):
        self.image = img
        self.rect  = Rect(self.position.x, self.position.y, img.get_width(), img.get_height())
    
    # Set waypoint list    
    def setWaypointList(self, wpList):
        self.wayPoints = wpList
        # Recalc direction
        self.activeWaypointIndex = 0
        targetVector             = self.wayPoints[ self.activeWaypointIndex ]
        self.direction           = Vector2D.fromPoints( self.position, targetVector )
        self.direction.normalizeVector() 
        
    # Updates position
    def update(self, timePassed):
        self.position += self.direction * ( timePassed * self.unitSpeed )
        
        x = self.position.x
        y = self.position.y 
        self.rect.left = x
        self.rect.top  = y
        
        # Recalc heading 
        dirX = self.direction.x 
        dirY = self.direction.y
        rad    = 0.5 - math.atan2( dirY, dirX ) 
        #print rad
        #print self.direction
        #exit()
        
        self.activeDirectionIndex = int( rad * 16 )
        self.checkWaypoints() 
        
    # Check if new waypoint is reached
    def checkWaypoints(self):
        if self.wayPoints is not None:  
            # Compare distance between targetVector and currentPosition
            targetVector             = self.wayPoints[ self.activeWaypointIndex ]
            distance                 = Vector2D.fromPoints( self.position, targetVector )
            if distance.getVectorLength() < 10:
                
                self.activeWaypointIndex = (self.activeWaypointIndex + 1) % len( self.wayPoints )
                # Change to new direction
                targetVector             = self.wayPoints[ self.activeWaypointIndex ]
                # print "moving to next Waypoint " + str( targetVector )
                self.direction           = Vector2D.fromPoints( self.position, targetVector )
                self.direction.normalizeVector() 
      
    # Returns the current animationMode As String
    def getAnimationModeAsString(self):
        strRes = str( self.animationMode )
        if len( strRes ) == 1:
            return "000" + strRes 
        else:
            return "00" + strRes 
       
    # Render Gameentitiy 
    def render(self, surface, renderRect ): 
        
        if self.image is not None:
            surface.blit( self.image, renderRect ) 
            
        #txtSurface = self.infoSurface.render( "%s,%s"%renderRect.topleft, True, (255,255,255)) 
        #surface.blit( txtSurface, renderRect.topleft )
    
    