class menu_settings:
    """settings menu"""
    def __init__(self, xml):
        self.reload(xml)

    def reload(self, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def printVal(self, elt):
        log.debug(elt['value'])

    def setGame(self):
        manager.controls.setFocusGame()

    def setMenu(self):
        manager.controls.setFocusMenu()

    def savesettings(self):
        pass
