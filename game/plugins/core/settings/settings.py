import xml.etree.ElementTree as et
from xml.dom import minidom


class Settings:
    """Settings manager"""
    def __init__(self, manager, xml):
        self.manager = manager
        #self.xml = xml
        self.settingsConfigDir = "config/settings/"
        self.ctrlConfig = et.parse(self.settingsConfigDir + 'controls.xml')

        self.controlTypes = ['game', 'menu']
        #perhaps loadSettings shoudl actually be reload????
        #self.reload()

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    #read all xml settings and set appropriate game variables
    def loadSettings(self, manager):
        #load settings from menu_settings.xml
        #is that a good place to store them?
        pass

    #take all game variables and modify xml files with them
    def save(self):
        self.saveControls()
        self.saveSettings()

    def saveSettings():
        #rewrite menu_settings.xml to update proper values
        pass

    #return ALL the controls in a dict - key, callback
    def getControls(self):
        controls = {}

        for ctrlType in self.controlTypes:
            controls[ctrlType] = {}
            try:
                ctrlTypeXml = self.ctrlConfig.find(ctrlType)
            except:
                print "couldn't find focus: ", ctrlType

            for plugin in ctrlTypeXml.findall("*"):
                controls[ctrlType][plugin.tag] = []
                for act in plugin.findall('action'):
                    controls[ctrlType][plugin.tag]
                    name = act.get('name')
                    key = act.get('key')
                    callback = act.get('callback')
                    controls[ctrlType][plugin.tag].append([name, key, callback])

        return controls

    def saveControls(self):
        ctrls = et.Element('config')
        controls = self.manager.get('controls').savedControls
        for ctrlType in self.controlTypes:
            xmlType = et.SubElement(ctrls, ctrlType)
            focus = controls[ctrlType]
            for plugin in focus:
                xmlPlugin = et.SubElement(xmlType, plugin)
                for action in focus[plugin]:
                    xmlAct = et.SubElement(xmlPlugin, 'action')
                    xmlAct.set('name', action[0])
                    xmlAct.set('key', action[1])
                    xmlAct.set('callback', action[2])

        ctrlFile = open(self.settingsConfigDir + 'controls.xml', 'w')
        ctrlFile.write(minidom.parseString(et.tostring(ctrls)).toprettyxml())
        ctrlFile.close()
