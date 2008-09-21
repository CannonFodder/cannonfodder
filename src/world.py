import time
from game.universe import *

u = User()
w = World()

w.addUser(u)
while 1:
    w.iterate()
    time.sleep(1)