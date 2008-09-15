import math 

class Vector2D:
    
    x = 0
    y = 0
    
    def __init__(self,x=0.0,y=0.0):
        self.x = x
        self.y = y
        
    # to String method 
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)
    
    # Multiply by scalar     
    def __mul__(self, scalar):
        return Vector2D( self.x * scalar, self.y * scalar )
        
    # divide through scalar
    def __div__(self, scalar):        
        return Vector2D( self.x / scalar, self.y / scalar )
        
    # Add a second vector
    def __add__(self, secondVector):
        return Vector2D( self.x + secondVector.x, self.y + secondVector.y )
     
    # Subtract a second vector    
    def __sub__(self, secondVector):
        return Vector2D( self.x - secondVector.x, self.y - secondVector.y ) 
    
    # Negate vector
    def __neg__(self):
        return Vector2D( -self.x, -self.y )
        
    # Retrieve vector-length
    def getVectorLength(self):
        return math.sqrt( self.x**2 + self.y**2 )
    
    # Normalize vector
    def normalizeVector(self):
        vectorLength = self.getVectorLength()
        self.x /= vectorLength
        self.y /= vectorLength
    
   
    @classmethod
    # Calculate direction-vector by two vectors 
    def fromPoints( cls, vectorA, vectorB ):
        return cls( vectorB.x - vectorA.x , vectorB.y - vectorA.y )
        
        