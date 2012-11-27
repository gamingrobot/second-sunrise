#! /usr/bin/env python
#
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

# Entry point - sets up the plugin system by giving it the config file to load and then releases panda to do its thing...

# Important: this must be first
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, loadPrcFileData
loadPrcFile("config/settings/settings.prc")
#loadPrcFileData("window-disable", "window-type none")

from bin.manager import *

import sys
from bin.log import Log
from bin.events import Events


class Second_Sunrise(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Detect if we are in a multifile and, if so, jump through hoops that shouldn't exist...
        if base.appRunner != None:
            print 'In multifile, root = ' + base.appRunner.multifileRoot
            baseDir = base.appRunner.multifileRoot + '/'
        else:
            baseDir = ''

        #make logger global
        __builtins__.log = Log()

        #make events global
        __builtins__.events = Events()

        # Create the manager - this does it all...
        pluginmanager = Manager(baseDir)

        #make manager global
        __builtins__.manager = pluginmanager

        # Create a task to do the work of getting the game going...
        def firstLight(task):
            if len(sys.argv) > 1:
                cn = sys.argv[1]
            else:
                cn = 'menu_main'

            pluginmanager.transition(cn)
            return task.done

        taskMgr.add(firstLight, 'firstLight')
        #firstLight()


app = Second_Sunrise()
app.run()
