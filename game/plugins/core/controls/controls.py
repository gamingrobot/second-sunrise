from direct.showbase import DirectObject


class Controls(DirectObject.DirectObject):
    """Plugin for controlling the controls system"""
    """Todo:
    finalizeKeys(self, plugin)
        runs comparison between menu_controls and game_controls AND controls.xml
        removes anything from xml that hasn't been registered for the plugin
        developer must always call this after registering their last key, which should always be done in their init

    everything goes to controls.xml

    upon registerKey(Game|Menu)(), compare pluginName and callback name, overwrite any differences thus:
        use key from xml, use name from plugin Dev



    """
    def __init__(self, manager, xml):
        settings = manager.get("settings")
        self.savedControls = settings.getControls()
        self.controls = {}
        self.controls['menu'] = {}
        self.controls['game'] = {}
        #this should be false by default, but for now we're treating gameMode as All
        self._gameMode = True

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def setFocusMenu(self):
        self._gameMode = False
        for plugin in self.menu_controls:
            for name, key, callback in self.menu_controls[plugin]:
                self.accept(key, callback)
        for plugin in self.game_controls:
            for name, key, callback in self.game_controls[plugin]:
                self.ignore(key)

    def setFocusGame(self):
        self._gameMode = True
        for plugin in self.game_controls:
            for name, key, callback in self.game_controls[plugin]:
                self.accept(key, callback)
        for plugin in self.menu_controls:
            for name, key, callback in self.menu_controls[plugin]:
                self.ignore(key)

    def __registerKey(self, name, key, callback, plugin, focus):
        pluginName = plugin.__class__.__name__
        if not (plugin in self.controls[focus]):
            self.controls[focus][pluginName] = []

        if pluginName in self.savedControls[focus]:
            print "saved: ", self.savedControls[focus][pluginName], " name: ", callback.__name__
        self.controls[focus][pluginName].append([name, key, callback])
        if (focus == 'game' and self.inGameMode()) or (focus == 'menu' and self.inMenuMode):
            self.accept(key, callback)

    def registerKeyMenu(self, name, key, callback, plugin):
        self.__registerKey(name, key, callback, plugin, 'menu')

        '''pluginName = plugin.__class__.__name__
        if not (plugin in self.menu_controls):
            self.menu_controls[pluginName] = []

        if (pluginName in self.savedControls['menu'] and ):
        self.menu_controls[pluginName].append([name, key, callback])
        if self.inMenuMode():
            self.accept(key, callback)'''

    def registerKeyGame(self, name, key, callback, plugin):
        self.__registerKey(name, key, callback, plugin, 'game')

        '''pluginName = plugin.__class__.__name__
        if not (plugin in self.game_controls):
            self.game_controls[pluginName] = []
        self.game_controls[pluginName].append([name, key, callback])
        if self.inGameMode():
            self.accept(key, callback)
        print self.game_controls'''

    def registerKeyAll(self, name, key, callback, plugin):
        self.registerKeyGame(name, key, callback, plugin)
        self.registerKeyMenu(name, key, callback, plugin)

    def unRegisterKeyMenu(self, name, plugin):
        pass

    def unRegisterKeyGame(self, name, plugin):
        pass

    def unRegisterKeyAll(self, name, plugin):
        pass

    def reInitKeys(self):
        pass

    def inMenuMode(self):
        return not self._gameMode

    def inGameMode(self):
        return self._gameMode
