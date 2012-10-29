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

from direct.gui.DirectGui import *


class QuickMenu:
    """This creates a menu - nothing fancy - just a list of buttons, each of which invokes a transition to another config file."""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        self.buttons = []

        # Create the button objects...
        yPos = 0.8
        for but in xml.findall('button'):
            button = DirectButton(text=but.get('text', '-'), pos=(0.0, 0.0, yPos), scale=.065)
            yPos -= 0.1
            action = but.get('action')
            if action == "menu":
                pass

            elif action == "function":
                button['command'] = getattr(self, but.get('target'))

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

    def helloworld(self):
        print "helloworld"
