from game.gameEntity import GameEntity

class Explosion(GameEntity):

    totalTime = 0.0
    animationSpeed = 0.5
    
    def __init__(self, name, pos, animationSpeed):
        GameEntity.__init__(self, position=pos, name=name )
        self.animationSpeed = animationSpeed
        self.currentMode    = 'a'
        self.activeDirectionIndex = 0
        
    def update(self, timePassed):
        self.totalTime += timePassed
        if self.totalTime > self.animationSpeed:
            self.animationMode += 1 # Instead of direction
            if self.animationMode >= self.maxAnimationScenes:
                #print "no longer alive"
                self.isAlive = False
            self.totalTime = 0.0