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

import posixpath


class Global:
    """This provides global access to lumps of configuration xml - allows other plugin objects to get at the xml it is given."""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        self.xml = xml

        # Some clever code for handling being in a p3d file - turn paths into full paths if needed...
        if base.appRunner != None:
            for elem in self.xml:
                if 'path' in elem.attrib:
                    elem.attrib['path'] = posixpath.join(base.appRunner.multifileRoot, elem.attrib['path'])

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def getConfig(self):
        return self.xml
