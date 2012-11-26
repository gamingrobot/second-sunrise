# -*- coding: utf-8 -*-
# Copyright Tom SF Haines
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from panda3d.core import *
from direct.actor import Actor


class Loading:
    """Does a loading screen - renders some stuff whilst a transition is happenning."""
    def __init__(self, xml):
        self.node = Actor.Actor('data/misc/loading')
        self.node.reparentTo(base.render)
        self.node.setShaderAuto()
        self.node.hide()

        self.light = PointLight('plight')
        self.light.setColor(VBase4(1.0, 1.0, 1.0, 1.0))
        self.lightNode = self.node.attachNewNode(self.light)
        self.lightNode.setPos(0.0, 0.0, 1.5)
        self.node.setLight(self.lightNode)

        self.task = None

        #self.stop()

    def reload(self, xml):
        pass

    def start(self):
        self.node.hide()
        self.node.stop()

        if self.task != None:
            taskMgr.remove(self.task)
            self.task = None

    def stop(self):
        self.node.show()
        self.node.loop('slide')
        self.task = taskMgr.add(self.camPos, 'LoadingCamera')

    def destroy(self):
        pass

    def camPos(self, task):
        base.camera.setPos(0.0, 0.0, 20.0)
        base.camera.lookAt(0.0, 0.0, 0.0)
        return task.cont
