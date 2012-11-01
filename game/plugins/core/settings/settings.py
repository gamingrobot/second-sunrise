import xml.etree.ElementTree as et


class Settings:
    """Settings manager"""
    def __init__(self, manager, xml):
        self.manager = manager
        #self.xml = xml
        self.settingsConfigDir = "config/settings/"
        self.ctrlConfig = et.parse(self.settingsConfigDir + 'controls.xml')

        #perhaps loadSettings shoudl actually be reload????
        #self.reload()

    def reload(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    #read all xml settings and set appropriate game variables
    def loadSettings(self, manager):
        #load controls.xml, set appropriate in-game and
        #in-menu controls via controls plugin
        #also load game-wide controls
        #load settings from menu_settings.xml
        #is that a good place to store them?
        pass

    #take all game variables and modify xml files with them
    def saveSettings(self):
        pass

    #return ALL the controls in a dict - key, callback
    def getControls(self):
        controls = {}

        controlTypes = ['game', 'menu']

        for ctrlType in controlTypes:
            controls[ctrlType] = {}
            try:
                ctrlTypeXml = self.ctrlConfig.find(ctrlType)
            except:
                print "couldn't find focus: ", ctrlType

            for plugin in ctrlTypeXml.findall("*"):
                    for act in plugin.findall('action'):
                        controls[ctrlType][plugin.tag] = []
                        name = act.get('name')
                        key = act.get('key')
                        callback = act.get('callback')
                        controls[ctrlType][plugin.tag].append([name, key, callback])

        return controls
