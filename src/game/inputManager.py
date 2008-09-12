import pygame 
from pygame.locals import * 

class InputManager:
    
    myActiveGameScene = None
    
    def __init__( self ):
        pass
    
    # Transform eventType to String
    def eventTypeToString(self,eventType):
        if eventType == MOUSEBUTTONDOWN or eventType == KEYDOWN:
            return "PRESSED"
        else:
            return "RELEASED"
    
    # Handle input Events , delegate to active gameScene
    def handleInput( self,events ):
        
        if self.myActiveGameScene is not None:
            for eachEvent in events:
                eventType = eachEvent.type
                
                # Check for keyboard input
                if eventType == KEYDOWN or eventType == KEYUP:
                    self.myActiveGameScene.handleKeyInput( eachEvent.key, eachEvent.mod, self.eventTypeToString(eventType) )
                elif eventType == MOUSEMOTION:
                    pass
                elif eventType == MOUSEBUTTONDOWN or eventType == MOUSEBUTTONUP:
                    self.myActiveGameScene.handleMouseInput( eachEvent.button, self.eventTypeToString(eventType) )
        
    def setActiveGameScene(self, gameScene):
        self.myActiveGameScene = gameScene