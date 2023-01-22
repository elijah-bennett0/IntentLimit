# -*- coding: utf-8 -*-
"""
@Description		: CTRLALTECH Main Toolbox
@Author			: Ginsu
@Date			: 2023014
@Version		: 2023.0.1
"""

### Imports
import os
import code
from resources.env import *
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
addPath(PLUGIN_DIR)
addPath(TOOL_DIR)

# This is to add the path of each tool individually.
# Did this because the __import__ method was not working with tool loading.
# Maybe find a more elegant way to do this?
for cat in os.listdir(TOOL_DIR):
	for tool in os.listdir(os.path.join(TOOL_DIR, cat)):
		addPath(os.path.join(TOOL_DIR, cat, tool))
###

### Local Imports
import exception
from ilcmd import *
from iohandler import *
from pluginManager import *
###

### Code
def loadAll(il):
	il.manager.loadPlugins()
	il.manager.loadTools()

def python(il):
	il.io.Print('i', "Dropping to Python, CTRL-D to exit")
	code.interact(banner="IntentLimit Python Interpreter")

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
	global il
	il = IntentLimit(config, ildir, PLUGIN_DIR, TOOL_DIR)
	loadAll(il)
	main(il)
###

if __name__ == "__main__":
	run(IL_CONFIG, IL_DIR)
