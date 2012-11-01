from direct.gui.DirectGui import *
import xml.etree.ElementTree as et


class Menu:
    """menu manager"""
    def __init__(self, manager, xml):
        self.frames = []
        self.directObjects = []
        self.menuConfigDir = "config/menu/"
        self.menuCodeDir = "plugins.core.menu.controllers"
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
                #base = self.menuCodeDir + '.' + self.currentMenu.lower()
                #menu = __import__(base, globals(), locals(), [self.currentMenu.lower()])
                #menu = getattr(menu, self.currentMenu)
                #print menu
                #inst = getattr(menu, self.currentMenu)(manager, xml)  # Init
                button['command'] = self.getFunc(manager, xml, but, 'target')

            elif action == "config":
                button['command'] = manager.transition
                button['extraArgs'] = [but.get('target')]

            elif action == "event":
                button['command'] = manager.get('events').triggerEvent
                button['extraArgs'] = [but.get('target'), {}]
            button.hide()
            self.directObjects.append(button)

        for sldr in xml.findall('slider'):
            try:
                low = sldr.get('min')
            except:
                low = 0
            try:
                high = sldr.get('max')
            except:
                high = 100
            try:
                step = sldr.get('step')
            except:
                step = 0.01

            #get the function based on the attribute onchange
            func = self.getFunc(manager, xml, sldr, 'onchange')
            slider = DirectSlider(range=(float(low), float(high)), value=float(sldr.get('value')), pageSize=float(step), command=func)
            slider['extraArgs'] = [slider]
            yPos -= 0.1

            slider.hide()
            self.directObjects.append(slider)

        '''for fld in xml.findall('input'):
            field = DirectEntry(parent)

            field.hide()
            self.directObjects.append(field)'''

    def start(self):
        for obj in self.directObjects:
            obj.show()

    def stop(self):
        for obj in self.directObjects:
            obj.hide()

    def destroy(self):
        for obj in self.directObjects:
            obj.destroy()

    def getFunc(self, manager, xml, el, attr):
        base = self.menuCodeDir + '.' + self.currentMenu.lower()
        menu = __import__(base, globals(), locals(), [self.currentMenu.lower()])
        inst = getattr(menu, self.currentMenu)(manager, xml)  # Init controller
        return getattr(inst, el.get(attr))  # function call

    def changeMenu(self, manager, target):
        xml = et.parse(self.menuConfigDir + target + '.xml')
        self.currentMenu = target
        self.destroy()
        self.directObjects = []
        self.reload(manager, xml)
        self.start()
