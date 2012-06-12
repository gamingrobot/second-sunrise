from panda3d.rocket import *
from direct.directbase import DirectStart

LoadFontFace("assets/Delicious-Roman.otf")

r = RocketRegion.make('pandaRocket', base.win)
r.setActive(1)
context = r.getContext()

context.LoadDocument('data/background.rml').Show()

doc = context.LoadDocument('data/main_menu.rml')
doc.Show()

ih = RocketInputHandler()
base.mouseWatcher.attachNewNode(ih)
r.setInputHandler(ih)


def OnClick():
  for i in range(10):
    print('Line ' + str(i))

element = doc.GetElementById('test')
element.AddEventListener('click', OnClick, True)

run()
