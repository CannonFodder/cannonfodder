import random
from math import sin,cos,pi
import md5
import string
from twisted.spread import pb
from utils.vector import Vector2D, Angle, Rectangle, RotationMatrix2D

class User(object):
    def __init__(self):
        self.rectangle = Rectangle(Vector2D(0,0),Vector2D(1000,1000))
        self.lastUpdateEntities = []
    def updateEntitiesInViewport(self, entities):
        updateEntities = []
        for entity in entities:
            if self.rectangle.covers(entity.position,entity.length):
                updateEntities.append(entity)
        for lastEntity in self.lastUpdateEntities:
            if not updateEntities.__contains__(lastEntity):
                self.deactivateEntity(lastEntity)
        for entity in updateEntities:
            if not self.lastUpdateEntities.__contains__(entity):
                self.activateEntity(entity)
            else:
                self.updateEntity(entity)
        self.lastUpdateEntities = updateEntities
    def updateEntity(self, entity):
        pass
    def deactivateEntity(self,entity):
        pass
    def activateEntity(self,entity):
        pass

class Entity(pb.RemoteCopy,pb.Copyable):
    def __init__(self):
        self.position = Vector2D(0,0)
        self.length = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.direction = Angle(0)
        self.active = True
        m = md5.new()
        m.update(str(random.random()))
        self.id =  m.hexdigest()
        print "new entity width id #"+self.id
    def iterate(self):
        pass
    def setPosition(self,x,y):
        self.position = Vector2D(x,y)
    def isDead(self):
        return False
    def __str__(self):
        return str(self.id)

pb.setUnjellyableForClass(Entity, Entity)
                           
class KreiselDepp(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.velocity = Vector2D(1.0,0.0)
        self.length = Vector2D(10,10)
        self.directionDegree = 10.0
    def iterate(self):
        self.direction.add( self.directionDegree )
        self.velocity = RotationMatrix2D().rotate(Vector2D(2,0),self.direction)
        self.position += self.velocity

pb.setUnjellyableForClass(KreiselDepp, KreiselDepp)

class Map(object):
    pass

class World(object):
    def __init__(self):
        self.entities = []
        self.users = []
        e = Entity()
        e.position = Vector2D(100,100)
        self.addEntity(e)
        e = KreiselDepp()
        e.position = Vector2D(50,50)
        e.directionDegree = -4
        self.addEntity(e)
        e = KreiselDepp()
        e.position = Vector2D(70,30)
        self.addEntity(e)
    def addEntity(self, entity):
        self.entities.append(entity)
    def removeEntity(self, entity):
        self.entities.remove(entity)
    def addUser(self, user):
        self.users.append(user)
    def removeUser(self, user):
        self.users.remove(user)
    def iterate(self):
        for entity in self.entities:
            entity.iterate()
        for user in self.users:
            user.updateEntitiesInViewport(self.entities)
        for entity in self.entities:
            if entity.isDead():
                self.removeEntity(entity)
