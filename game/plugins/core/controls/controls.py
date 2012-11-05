from direct.showbase import DirectObject


class Controls(DirectObject.DirectObject):
    """Plugin for controlling the controls system"""
    """Todo:
    finalizeKeys(self, plugin)
        runs comparison between menu_controls and game_controls AND controls.xml
        removes anything from xml that hasn't been registered for the plugin
            basically set self.savedControls = self.controls with the exception that the final array[2] should be the name instead of the method reference
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

    def __setFocus(self, focus):
        if (focus == 'game'):
            self._gameMode = True
            one = 'game'
            two = 'menu'
        else:
            self._gameMode = False
            one = 'menu'
            two = 'game'


        for plugin in self.controls[two]:
            for name, key, callback in self.controls[two][plugin]:
                self.ignore(key)
        for plugin in self.controls[one]:
            for name, key, callback in self.controls[one][plugin]:
                self.accept(key, callback)

    def setFocusMenu(self):
        self.__setFocus('menu')

    def setFocusGame(self):
        self.__setFocus('game')

    def __registerKey(self, name, key, callback, plugin, focus):
        pluginName = plugin.__class__.__name__
        curFocus = self.controls[focus]
        savedFocus = self.savedControls[focus]
        if not (pluginName in curFocus):
            curFocus[pluginName] = []
        if not (pluginName in savedFocus):
            savedFocus[pluginName] = []

        plugin = curFocus[pluginName]
        savedPlugin = savedFocus[pluginName]
        found = False

        for action in savedPlugin:
            if action[2] == callback.__name__:
                key = action[1]
                action = [name, key, callback.__name__]
                print "action ", action
                global found
                found = True
                break

        if not found:
            savedPlugin.append([name, key, callback.__name__])

        plugin.append([name, key, callback])

        if (focus == 'game' and self.inGameMode()) or (focus == 'menu' and self.inMenuMode):
            self.accept(key, callback)

        return key

    def registerKeyMenu(self, name, key, callback, plugin):
        return self.__registerKey(name, key, callback, plugin, 'menu')

    def registerKeyGame(self, name, key, callback, plugin):
        return self.__registerKey(name, key, callback, plugin, 'game')

    def registerKeyAll(self, name, key, callback, plugin):
        keyGame = self.registerKeyGame(name, key, callback, plugin)
        keyMenu = self.registerKeyMenu(name, key, callback, plugin)
        ret = {}
        ret["game"] = keyGame
        ret["menu"] = keyMenu
        return ret

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