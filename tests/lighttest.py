import direct.directbase.DirectStart
from panda3d.core import *
 
# Put two pandas in the scene, panda x and panda y.
x = loader.loadModel('panda')
x.reparentTo(render)
x.setPos(10,0,-6)
 
y = loader.loadModel('panda')
y.reparentTo(render)
y.setPos(-10,0,-6)
 
# Position the camera to view the two pandas.
base.trackball.node().setPos(0, 60, 0)
 
# Now create some lights to apply to everything in the scene.
 
# Create Ambient Light
#ambientLight = AmbientLight('ambientLight')
#ambientLight.setColor(Vec4(0.1, 0.1, 0.1, 1))
#ambientLightNP = render.attachNewNode(ambientLight)
#render.setLight(ambientLightNP)
 
# Directional light 01
directionalLight = DirectionalLight('directionalLight')
directionalLight.setColor(Vec4(0.8, 0.2, 0.2, 1))
directionalLightNP = render.attachNewNode(directionalLight)
# This light is facing backwards, towards the camera.
directionalLightNP.setHpr(180, -20, 0)
render.setLight(directionalLightNP)
 
# Directional light 02
directionalLight = DirectionalLight('directionalLight')
directionalLight.setColor(Vec4(0.2, 0.2, 0.8, 1))
directionalLightNP = render.attachNewNode(directionalLight)
# This light is facing forwards, away from the camera.
directionalLightNP.setHpr(0, -20, 0)
render.setLight(directionalLightNP)
 
# Now attach a green light only to object x.
ambient = AmbientLight('ambient')
ambient.setColor(Vec4(0.5, 1, 0.5, 1))
ambientNP = x.attachNewNode(ambient)
 
# If we did not call setLightOff() first, the green light would add to
# the total set of lights on this object. Since we do call
# setLightOff(), we are turning off all the other lights on this
# object first, and then turning on only the green light.
x.setLightOff()
x.setLight(ambientNP)
 
#run the example
run()