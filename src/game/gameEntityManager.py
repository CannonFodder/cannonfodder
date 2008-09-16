from game.gameEntity import GameEntity
from game.explosion import Explosion
from utils.utils import Utils 

class GameEntityManager:
    
    gameEntities = None
    lastEntityId = 0 
    myImgMngr    = None
    deathList    = None
    
    # Initialize 
    def __init__(self):
        self.gameEntities = {}
        self.deathList    = []
        
    # Add Entitiy 
    def addEntity(self, gameEntity):
        self.gameEntities[self.lastEntityId] = gameEntity
        gameEntity.id = self.lastEntityId
        self.lastEntityId += 1
    
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
    
    # Create new explosion
    def createExplosion( self, name, pos, animationSpeed ):
        self.loadUnit( name )
        someExplosion = Explosion( name, pos, animationSpeed )
        someExplosion.maxAnimationScenes = self.myImgMngr.getMaxAnimationScenes( name, 'a' )
        self.addEntity( someExplosion )
        return someExplosion
    
    # Update Entities 
    def update(self, timePassed):
        # Loop through deathlist
        for eachDeathId in self.deathList:
            self.removeEntity( eachDeathId )
        
        # Check every entity on list 
        for eachEntity in self.gameEntities.itervalues():
            if eachEntity.isAlive is True:
                eachEntity.update(timePassed)
            else:
                # if not alive put to deathlist 
                self.deathList.append( eachEntity.id )
            
    # Render every entities 
    def render(self, surface, viewPortRect ):
        for eachEntity in self.gameEntities.values():
            if eachEntity.activeDirectionIndex != -1:
                
                currentMode = eachEntity.currentMode 
                max = self.myImgMngr.getMaxAnimationScenes( eachEntity.name, currentMode )
                
                if int(max) > 0:
                    rotationMode = int( eachEntity.activeDirectionIndex ) % int( max )
                else:
                    rotationMode = int( eachEntity.activeDirectionIndex )
                    
                someStr = str( rotationMode )
                #rotationMode   = eachEntity.getRotationModeAsString()
                strAnimationMode = eachEntity.getAnimationModeAsString()
                
                # Which mode?
                if len( someStr ) == 1:
                    someStr = "000" + someStr
                else:
                    someStr = "00"  + someStr 

                activeImage = self.myImgMngr.getImage( eachEntity.name, currentMode,  someStr, strAnimationMode )
                
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