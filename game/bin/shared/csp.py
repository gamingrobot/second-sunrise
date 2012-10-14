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



# Custom string parsers, for turning certain config parameters into useful data.

from pandac.PandaModules import *


def getPos(s):
  """Given a string in a form "5,4,3" returns a Vec3 for that vector."""
  n = map(lambda x:float(x),s.split(','))
  if len(n)!=3:
    raise Exception('Bad vector string')
  return Vec3(n[0],n[1],n[2])