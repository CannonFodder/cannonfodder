from game.gameScene import GameScene

class MainGameScene( GameScene ):
    
    def handleMouseInput(self, mousebutton, state = 'PRESSED'):
        print "mouseInput :: " + str( mousebutton ) + "," + state 
    
    def handleKeyInput(self, key, modifier, state = 'PRESSED' ):
        print "key :: " + str(key) + "," + str(modifier) + "," + state