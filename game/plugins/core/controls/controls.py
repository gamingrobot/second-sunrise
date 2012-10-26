from direct.showbase import DirectObject


class Controls(DirectObject.DirectObject):
    """Plugin for controlling the controls system"""
    def __init__(self, manager, xml):
        self.menu_controls = {}
        self.game_controls = {}

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def setFocusGame():
        pass

    def setFocusMenu():
        pass

    def registerKeyMenu(self, name, key, callback, plugin):
        pass

    def registerKeyGame(self, name, key, callback, plugin):
        if not (plugin in self.game_controls):
            self.game_controls[plugin] = []
        self.game_controls[plugin].append([name, key, callback])
        self.accept(key, callback)

    def registerKeyAll(self, name, key, callback, plugin):
        pass

    def unRegisterKeyMenu(self, name, callback, plugin):
        pass

    def unRegisterKeyGame(self, name, callback, plugin):
        pass

    def unRegisterKeyAll(self, name, callback, plugin):
        pass
