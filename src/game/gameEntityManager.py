from game.gameEntity import GameEntity
from utils.utils import Utils 

class GameEntityManager:
    
    gameEntities = None
    lastEntityId = 0 
    myImgMngr    = None
    
    # Initialize 
    def __init__(self):
        self.gameEntities = {}
        
    # Add Entitiy 
    def addEntity(self, gameEntity):
        self.gameEntities[self.lastEntityId] = gameEntity
        self.lastEntityId += 1
        return self.lastEntityId - 1
    
    # Remove Entity 
    def removeEntity(self, entityId):
        del self.gameEntities[entityId]
        
    # Request gameEntity 
    def getEntity(self, entityId):
        return self.gameEntities[entityId]
    
    # Load unit (donnot create unit) 
    def loadUnit(self, name):
        print "Adding unit-directory " + name 
        self.myImgMngr.addUnitDirectory( name )
        
    # Load unit (images with intial pos, dir and speed. Attach new GameEntity to manager 
    def loadAndCreateUnit(self, name, pos, dir, unitSpeed):
        self.loadUnit( name )
        newGameEntity = GameEntity(pos, dir, unitSpeed, name) 
        self.addEntity( newGameEntity )
        return newGameEntity
    
    # Update Entities 
    def update(self, timePassed):
        for eachEntity in self.gameEntities.itervalues():
            eachEntity.update(timePassed)
            
    def render(self, surface, viewPortRect ):
        for eachEntity in self.gameEntities.values():
            if eachEntity.activeDirectionIndex != -1:
                
                max = self.myImgMngr.getMaxAnimationScenes( eachEntity.name, 'r' )
                rotationMode = int( eachEntity.activeDirectionIndex ) % int( max )
                someStr = str( rotationMode )
                animationMode = "0000"
                
                # Which mode?
                if len( someStr ) == 1:
                    someStr = "000" + someStr
                else:
                    someStr = "00"  + someStr 

                activeImage = self.myImgMngr.getImage( eachEntity.name, 'r',  someStr, animationMode )
                
                if activeImage is not None:
                    # Set activeImage to entity 
                    eachEntity.setImage( activeImage )  
                
            renderRect = Utils.transformRectPosition( eachEntity.rect, viewPortRect )
            
            # Visibility test to avoid unnescary rendering
            if eachEntity.checkVisibility is True:
                entityRect = eachEntity.rect
                if viewPortRect.collidepoint( entityRect.topleft ) or viewPortRect.collidepoint( entityRect.bottomright ):
                   eachEntity.render( surface, renderRect )                 
            else:
                eachEntity.render( surface, renderRect )