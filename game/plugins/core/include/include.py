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

import xml.etree.ElementTree as et


class Include:
    """Meta plugin that allows you to include other config files, will be declared as <obj type="Include" config="other"/> A name is not needed."""
    def __init__(self, xml):
        # Get the name of the config to load...
        self.config = xml.get('config')

    def postInit(self):
        # Load the configuration xml file...
        elem = et.parse(manager.getConfigDir() + self.config + '.xml')
        yield None

        # Iterate the relevant elements and use the manager to load them all...
        for obj in elem.findall('obj'):
            for blah in manager.addObj(obj):
                yield None

    def reload(self, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass
