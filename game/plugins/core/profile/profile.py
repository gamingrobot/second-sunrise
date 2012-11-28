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

import subprocess

from direct.showbase import DirectObject
from panda3d.core import PStatClient


class Profile(DirectObject.DirectObject):
    """Connects to pstats, if pstats is not running on the local computer it will set a copy running regardless."""
    def __init__(self, xml):
        self.pstats = None
        #TODO: register key to link to function go
        manager.controls.registerKeyGame("Open Profiler", "f2", self.go, self)

    def reload(self, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        if self.pstats != None:
            self.pstats.kill()

    def go(self):
        if (PStatClient.connect() == 0):
            # No pstat server - create it, then try and connect again...
            self.pstats = subprocess.Popen(['pstats'])

            # Need to give pstats some time to warm up - use a do latter task...
            def tryAgain(task):
                PStatClient.connect()
            taskMgr.doMethodLater(0.5, tryAgain, 'pstats again')
