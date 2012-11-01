# -*- coding: utf-8 -*-
# Copyright 2009 Reinier de Blois, Tom SF Haines
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

from panda3d.core import AntialiasAttrib
from panda3d.core import WindowProperties
from panda3d.core import ClockObject
import datetime


class Window:
    """This plugin sets up window properties"""
    def __init__(self, manager, xml):
        render.setAntialias(AntialiasAttrib.MAuto)
        base.setBackgroundColor(100 / 255.0, 149 / 255.0, 237 / 255.0)
        render.setTwoSided(True)
        base.toggleWireframe()

        self.task = None

        # Get supported resolutions...
        info = base.pipe.getDisplayInformation()
        self.res = []
        for i in xrange(info.getTotalDisplayModes()):
            self.res.append((info.getDisplayModeWidth(i), info.getDisplayModeHeight(i)))

    def reload(self, manager, xml):
        pass

    screenshot = lambda self: base.screenshot()
    wireframe = lambda self: base.toggleWireframe()

    def toggleFullscreen(self):
        prop = base.win.getProperties()
        newProp = WindowProperties()

        if not prop.getFullscreen():
            newProp.setFullscreen(True)
            # Quick hack to get it to select a suitable display mode.
            if (1920, 1080) in self.res:
                newProp.setSize(1920, 1080)
            elif (1680, 1050) in self.res:
                newProp.setSize(1680, 1050)
            elif (1280, 768) in self.res:
                newProp.setSize(1280, 768)
            elif (1024, 768) in self.res:
                newProp.setSize(1024, 768)
            else:
                newProp.setSize(800, 600)
        else:
            newProp.setFullscreen(False)

        base.win.requestProperties(newProp)

    def record(self, task):
        base.screenshot(defaultFilename=False, namePrefix=('video|%s|%04i.jpg' % (self.video, self.frameNum)))
        self.frameNum += 1
        return task.cont

    def toggleRecording(self):
        if self.task == None:
            self.frameNum = 0
            self.video = datetime.datetime.now().strftime('%Y-%m-%d|%H:%M:%S')
            self.task = taskMgr.add(self.record, 'RecordFrames')
            globalClock.setMode(ClockObject.MNonRealTime)
            globalClock.setFrameRate(25.0)
            print 'started recording'
        else:
            globalClock.setMode(ClockObject.MNormal)
            taskMgr.remove(self.task)
            self.task = None
            print 'ended recording'
