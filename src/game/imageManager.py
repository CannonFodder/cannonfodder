import pygame 
# from os import * 
import os 

class ImageManager:
    
    imgList     = {}
    maxAnimationDict = {}
    textureList = {}
    lastImgId   = 0
    GFX_DIRECTORY = "../data/gfx/"
    
    def __init__(self):
        # os.path.join("../data/gfx")
        pass
    
    # Load heightmap 
    def loadHeightmap(self, name):
        absPath = os.path.abspath( self.GFX_DIRECTORY + "/level")
        return pygame.image.load( absPath + "/" + name + ".jpg" ).convert() 
        
    
    # Load terrain textures
    def loadTerrainTextures(self):
        absPath = os.path.abspath( self.GFX_DIRECTORY + "/terrain" )
        
        for eachFolder in os.listdir( absPath ):
            print "found folder :: " + eachFolder
            textureFolder = absPath + "/" + eachFolder
            for eachTextureFile in os.listdir( textureFolder ):
                print "found texture " + eachTextureFile
                fullFileName = os.path.join( textureFolder, eachTextureFile )
                try:
                    tex = pygame.image.load( fullFileName )
                    if tex.get_alpha() is None:
                        tex = tex.convert()
                    else:
                        tex = text.convert_alpha()
                    self.textureList[ eachTextureFile ] =  { 'group': textureFolder, 'file': eachTextureFile, 'texture': tex }
                except pygame.error,msg:
                    print "Coulnot load terrain texture " + eachTextureFile
                    
    # Request Texure by name 
    def getTextureByName(self, name):
        for eachTexture in self.textureList.values():
            if eachTexture['file'] == name:
                return eachTexture['texture']
            
        return None 
    
    # Add Image for Unit-Directory 
    def addUnitDirectory(self, name):
        
        if self.unitPathLoaded( name ) is False:        
            absPath = os.path.abspath( self.GFX_DIRECTORY ) + "/" + name 
            
            self.maxAnimationDict[ name ] = {'a':0,'r':0}
            
            for eachFile in sorted(os.listdir( absPath )):
                # create full filename 
                fullFileName = os.path.join( absPath, eachFile )
                try:
                    img = pygame.image.load( fullFileName )
                    if img.get_alpha() is None:
                        img = img.convert()
                    else:
                        img = img.convert_alpha()
                    
                    # Specify mode and modenumber
                    mode = eachFile[0:1]
                    modeNumber = eachFile[1:5]
                    
                    print "loaded file " + eachFile
                    
                    # Add to image list
                    self.imgList[ self.lastImgId ] = { 'id':self.lastImgId, 'name':name, 'img':img, "mode":mode, "modeNumber":modeNumber }
                    self.lastImgId += 1
                    
                    # Store max animation phases
                    if self.maxAnimationDict[ name ][ mode ] < modeNumber:
                        self.maxAnimationDict[ name ][ mode ] = modeNumber
                        
                except pygame.error,e:
                    print "error loading file " + eachFile
    
    # Return max animation scenes
    def getMaxAnimationScenes(self, name, mode):
        if len( name ) > 0 and len( mode ) > 0:
            if self.maxAnimationDict[ name ] is not None:
                return self.maxAnimationDict[ name ][ mode ]
        
        return 1
                    
    # Has unit been loaded
    def unitPathLoaded(self, name):
        for eachImage in self.imgList.values():
            if eachImage['name'] == name:
                return True
            
        return False 
            
    # Retrieve Image
    def getImage(self, name, mode = "r", modeNumber = "0001", animationMode = "0000"):
        for eachImage in self.imgList.values():
            if eachImage['name'] == name and eachImage['mode'] == mode and eachImage['modeNumber'] == modeNumber:
                return eachImage['img'] 
            
        return None
                
     
    
        
        