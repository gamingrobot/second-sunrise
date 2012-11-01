class menu_settings:
    """settings menu"""
    def __init__(self, manager, xml):
        self.manager = manager
        self.reload(manager, xml)

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def printVal(self, elt):
        print "Hi"
        print elt['value']

    def setGame(self):
        controls = self.manager.get("controls")
        controls.setFocusGame()

    def setMenu(self):
        controls = self.manager.get('controls')
        controls.setFocusMenu()

    def savesettings(self):
        pass
