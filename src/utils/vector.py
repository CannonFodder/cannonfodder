from twisted.spread import pb
import math 

class Angle(object):
    def __init__(self,angle=0.0):
        self.angle = angle
        
    def __add__(self, degree):
        self.angle += degree
        if( self.angle > 360 ):
            self.angle -= 360
        
    def __sub__(self, degree):
        self.angle -= degree
        if( self.angle < -360 ):
            self.angle += 360
        
    def __str__(self):
        return str(self.angle)
    
    def toRadiant(self):
        return self.angle*math.pi/180
    
    def add(self, degree):
        self.__add__(degree)
    
    def sub(self, degree):
        self.__sub__(degree)
    
class RotationMatrix2D(object):
    def rotate(self, vector, angle):
        rad = angle.toRadiant()
        x = vector.x * math.cos(rad) + vector.y *-math.sin(rad)
        y = vector.x * math.sin(rad) + vector.y * math.cos(rad)
        return Vector2D(x,y)

    
class Rectangle(object):
    def __init__(self,position,length):
        self.position = position
        self.length = length
    def covers(self,position,length):
        # rechts auserhalb
        if position.x > self.position.x+self.length.x:
            return False
        # unten ausserhalb
        if position.y > self.position.y+self.length.y:
            return False
        # oben ausserhalb
        if position.y+length.y < self.position.y:
            return False
        #links ausserhalb
        if position.x+length.x < self.position.x:
            return False
        
        return True
        

class Vector2D(pb.RemoteCopy,pb.Copyable):
    
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
    
    def __len__(self):
        '''Length as a list is always two (x and y)'''
        return 2
    
    def __getitem__(self, x):
        '''Make vector indexable, e.g. v[0] == x'''
        if type(x) is slice:
            return (self.x,self.y)
        elif x == 0:
            return self.x
        elif x == 1:
            return self.y
            
    
    # Normalize vector
    def normalizeVector(self):
        vectorLength = self.getVectorLength()
        self.x /= vectorLength
        self.y /= vectorLength
    
   
    @classmethod
    # Calculate direction-vector by two vectors 
    def fromPoints( cls, vectorA, vectorB ):
        return cls( vectorB.x - vectorA.x , vectorB.y - vectorA.y )

pb.setUnjellyableForClass(Vector2D, Vector2D)
