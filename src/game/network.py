from zope.interface import implements

import sys

from game import universe
from twisted.internet.task import LoopingCall
from twisted.spread import pb
from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.cred import credentials

from utils.vector import Vector2D

import time

class ServerConsole(object):
    def __init__(self, avatar):
        self.avatar = avatar
    def parse(self, cmdline):
        args = cmdline.split(' ')
        command = args.pop(0).strip().lower()
        return command, args
    def call(self, command, args):
        try:
            cmd = getattr(self, 'command_'+command)
            return cmd(args)
        except:
            return None
    def execute(self, cmdline):
        command, args = self.parse(cmdline)
        return self.call(command, args)
    def command_ls(self, args):
        return "".join(args)
    def command_explosion(self, args):
        e = universe.KreiselDepp()
        e.setPosition(int(args[0]),int(args[1]))
        self.avatar.server.world.addEntity(e)
        return "ok"
    
class User(pb.Avatar,universe.User):
    def __init__(self, name):
        universe.User.__init__(self)
        self.name = name
        self.console = ServerConsole(self)
    def perspective_console(self, cmdline):
        print self.name,"exec",cmdline
        return self.console.execute(cmdline)
    def disconnect(self):
        self.detached()
        self.server.world.removeUser(self)
        print "Bye, bye "+self.name
    def attached(self, mind):
        self.remote = mind
    def detached(self):
        self.remote = None
    def updateEntity(self, entity):
        if self.remote != None:
            defer = self.remote.callRemote('updateEntity', entity)
            defer.addCallback(self.updated)
            defer.addErrback(self.error)
            pass
    def deactivateEntity(self,entity):
        if self.remote != None:
            defer = self.remote.callRemote('deactivateEntity', entity)
            defer.addCallback(self.updated)
            defer.addErrback(self.error)
            pass
    def activateEntity(self,entity):
        if self.remote != None:
            defer = self.remote.callRemote('activateEntity', entity)
            defer.addCallback(self.updated)
            defer.addErrback(self.error)
            pass
    def updated(self, ret):
        return None
    def error(self, why):
        #print "...",why
        return None

class Server(object):
    def __init__(self):
        self.avatars = {}
    def run(self):
        realm = MyRealm()
        realm.server = self
        p = portal.Portal(realm)
        check = checkers.InMemoryUsernamePasswordDatabaseDontUse()
        check.addUser('user1', 'pass1')
        check.addUser('user2', 'pass2')
        check.addUser('user3', 'pass3')
        check.addUser('user4', 'pass4')
        p.registerChecker(check)
        reactor.listenTCP(8800, pb.PBServerFactory(p))
        self.world = universe.World()
        self._loopMainIteration = LoopingCall(self.mainIteration)
        fps = 10.0
        self._loopMainIteration.start(1.0/fps)
        reactor.run()

    def mainIteration(self):
        self.world.iterate()

class MyRealm(object):
    implements(portal.IRealm)
    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        avatar = User(avatarId)
        avatar.server = self.server
        avatar.attached(mind)
        self.server.world.addUser(avatar)
        self.server.avatars[avatarId] = avatar
        print "welcome user",avatarId
        return pb.IPerspective, avatar, avatar.disconnect

class Client(pb.Referenceable):
    def __init__(self):
        self.perspective = None
    def remote_updateEntity(self, entity):
        return None
    def remote_deactivateEntity(self, entity):
        return None
    def remote_activateEntity(self, entity):
        return None
    def connect(self, host, port, user, password):
        factory = pb.PBClientFactory()
        reactor.connectTCP(host, port, factory)
        def1 = factory.login(credentials.UsernamePassword(user, password),client=self)
        def1.addCallback(self.connected)
        self._loopMainIteration = LoopingCall(self.mainIteration)
        self._loopMainIteration.start(0.04)
        self._loopHandleEvents = LoopingCall(self.handleEvents)
        self._loopHandleEvents.start(0.04)
        reactor.run()
    def exit(self):
        self._loopHandleEvents.stop()
        self._loopMainIteration.stop()
        reactor.stop()
    def mainIteration(self):
        pass
    def handleEvents(self):
        pass
    def connected(self, perspective):
        self.perspective = perspective
    def execute(self, cmdline, cb):
        if self.perspective:
            defer = self.perspective.callRemote('console',cmdline)
            defer.addCallback(self.executed,(cb))
            defer.addErrback(self.error)
    def executed(self, result, cb):
        cb(result)
    def error(self, why):
        return None
