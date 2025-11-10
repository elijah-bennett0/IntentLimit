# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2023 Elijah Bennett (Ginsu)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@Description		: CTRLALTECH Main Toolbox
@Author			: Ginsu
@Date			: 20230122
@Version		: 2023.0.3
"""

### Imports
import os
import code
from resources.env import *
from time import sleep
###

### Directory Setup
(IL_FILE, IL_DIR) = setupCorePaths(os.path.realpath(__file__))

RESOURCE_DIR = os.path.join(IL_DIR, "resources")
PLUGIN_DIR   = os.path.join(IL_DIR, "plugins")
TOOL_DIR     = os.path.join(IL_DIR, "tools")
IL_CONFIG    = os.path.join(IL_DIR, "config.yaml")
###

### Path Stuff
addPath(RESOURCE_DIR)
addPath(PLUGIN_DIR) # might not need these last two, idk dont feel like figuring it out rn
addPath(TOOL_DIR)

# This is to add the path of each tool/plugin individually.
# Did this because the __import__ method was not working.
# Maybe find a more elegant way to do this?
addPluginDirs(PLUGIN_DIR)
addToolDirs(TOOL_DIR)
###

### Local Imports
import exception
from ilcmd import *
from update import *
from iohandler import *
from pluginManager import *
###

### Code
def loadAll(il):
	il.manager.loadPlugins()
	il.manager.loadTools()

def python(il):
	il.io.Print('i', "Dropping to Python, CTRL-D to exit")
	code.interact(banner='')

def main(il):
	while True:
		try:
			il.cmdloop()
		except exception.Interpreter:
			python(il)
		except KeyboardInterrupt:
			il.io.Print('f', "User Aborted!")
			break
		else:
			break
@exception.ExceptionWrapped
def run(config, ildir):
	checkUpdate()
	sleep(3)
	global il
	il = IntentLimit(config, ildir, PLUGIN_DIR, TOOL_DIR)
	loadAll(il)
	main(il)
###

if __name__ == "__main__":
	run(IL_CONFIG, IL_DIR)
