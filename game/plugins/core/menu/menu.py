from direct.gui.DirectGui import *
import xml.etree.ElementTree as et


class Menu:
    """menu manager"""
    def __init__(self, manager, xml):
        self.frames = []
        self.buttons = []
        self.menuConfigDir = "plugins/core/menu/menu_configs/"
        self.menuCodeDir = "plugins.core.menu.menu_code"
        self.currentMenu = ""

        self.reload(manager, xml)

    def reload(self, manager, xml):
        #create frame
        #check if config= is set
        try:
            config = xml.get('config')
            xml = et.parse(self.menuConfigDir + xml.get('config') + '.xml')
            self.currentMenu = config
        except:
            pass

        #add buttons because config= is not set
        yPos = 0.8
        for but in xml.findall('button'):
            button = DirectButton(text=but.get('text', '-'), pos=(0.0, 0.0, yPos), scale=.065)
            yPos -= 0.1
            action = but.get('action')
            if action == "menu":
                button['command'] = self.changeMenu
                button['extraArgs'] = [manager, but.get('target')]

            elif action == "function":
                print self.currentMenu.lower()
                base = self.menuCodeDir + '.' + self.currentMenu.lower()
                menu = __import__(base, globals(), locals(), [self.currentMenu.lower()])
                #menu = getattr(menu, self.currentMenu)
                #print menu
                inst = getattr(menu, self.currentMenu)(manager, xml)
                button['command'] = getattr(inst, but.get('target'))

            elif action == "config":
                button['command'] = manager.transition
                button['extraArgs'] = [but.get('target')]

            elif action == "event":
                button['command'] = manager.get('events').triggerEvent
                button['extraArgs'] = [but.get('target'), {}]
            button.hide()
            self.buttons.append(button)

    def start(self):
        for button in self.buttons:
            button.show()

    def stop(self):
        for button in self.buttons:
            button.hide()

    def destroy(self):
        for button in self.buttons:
            button.destroy()

    def changeMenu(self, manager, target):
        xml = et.parse(self.menuConfigDir + target + '.xml')
        self.currentMenu = target
        self.destroy()
        self.buttons = []
        self.reload(manager, xml)
        self.start()
