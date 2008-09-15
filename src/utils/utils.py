from pygame.locals import * 

class Utils:
    
    # tranform rect position to absolut position (with the help of the viewport)
    @classmethod 
    def transformRectPosition( cls, rect, viewPort ):
        x = rect.left - viewPort.left
        y = rect.top - viewPort.top 
        
        return Rect( x, y, rect.width, rect.height )