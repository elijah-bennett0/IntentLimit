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

@Description		: Manages plug-in scripts from /plugins
@Author			: Ginsu
@Date			: 20230115
@Version		: 1.5
"""

### Imports
import os
import sys
from iohandler import *
from env import supportsColors
###

__all__ = ["Manager", "loadedPlugins", "loadedTools"]

global loadedPlugins
global loadedTools
loadedPlugins = {}
loadedTools   = {}

### Code
class Manager():
	def __init__(self, baseDir, plugDir, toolDir):
		'''
		Initial loading of plugins
		'''
		self.mainPath  = baseDir
		self.pluginDir = plugDir
		self.toolDir   = toolDir
		self.handler   = IOhandler(supportsColors())
		self.supported = {'.py':'', '.pl':'perl ', '.sh':'bash '}

	def loadPlugins(self):
		self.handler.Print('i', "Loading plugins...")

		for dir in os.listdir(self.pluginDir):
			if os.path.isdir(os.path.join(self.pluginDir, dir)) and not dir.startswith("_"):
				files = os.listdir(os.path.join(self.pluginDir, dir))
				for file in files:
					if os.path.splitext(file)[1] in self.supported and "init" not in file and not (file == "__pycache__"):
						try:
							name, t = os.path.splitext(file)
							# ehhhhhhhhhhhhh
							# still need to add this functionality to reload(), loadNew()
							if t == '.py':
								module = getattr(__import__("%s.%s"%(name,name),fromlist=["%s.%s"%(name,name)]), name)
								configPath = os.path.join(self.pluginDir, dir, "config.yaml")
								loadedPlugins[name] = [module, configPath]
							else:
								configPath = os.path.join(self.pluginDir, dir, "config.yaml")
								loadedPlugins[name] = [os.path.join(self.pluginDir, dir, name), self.supported[t]] # {'test':'perl '} shitty but should work for now
						except Exception as e:
							self.handler.Print('f', "Could Not Load: %s" % name)
							self.handler.Print('c', str(e))
		self.handler.Print('s', "Loaded {} plugin(s)".format(len(loadedPlugins)))

	def loadTools(self):
		self.handler.Print('i', "Loading tools...")
		categories = os.listdir(self.toolDir)
		for category in categories:
			toolNames = os.listdir(os.path.join(self.toolDir, category))
			for toolName in toolNames:
				tools = [x for x in os.listdir(os.path.join(self.toolDir, category, toolName)) if os.path.splitext(x)[1] in self.supported and "init" not in x and "template" not in x]
				for tool in tools:
					if os.path.splitext(tool)[1] == '.py':
						try:
							name, t = os.path.splitext(tool)
							module = getattr(__import__(name, fromlist=[name]), name)
							configPath = os.path.join(self.toolDir, category, toolName, "config.yaml")
							loadedTools[name] = [module, configPath]
						except Exception as e:
							self.handler.Print('f', "Could Not Load: %s" % name)
							self.handler.Print('c', str(e))
		self.handler.Print('s', "Loaded {} tool(s)\n".format(len(loadedTools)))

	def createPlugin(self, arg):
		'''
		Create the basic template for a plugin
		'''
		try:
			os.system("cp {}/template.py {}/{}.py".format(self.pluginDir, self.pluginDir, arg))
			self.handler.Print('s', "Plugin created.\n")
		except:
			self.handler.Print('f', "Could not create plugin.\n")

	def removePlugin(self, arg):
		'''
		Remove plugin

		'''
		yn = self.handler.get_input("Sure you want to delete? (y/n): ")
		if yn == 'y':
			valid = []
			for file in os.listdir(self.pluginDir):
				if arg in file:
					valid.append(file)
			if len(valid) > 1:
				self.handler.Print('w', "More than one file with this name exists:")
				[self.handler.Print('i', x) for x in valid]
				ext = self.handler.get_input("Extension: ")
			else:
				if os.path.isdir(arg):
					ext = ''
				else:
					ext = '.py' # .py is default
			try:
				os.system("rm -rf {}/{}".format(self.pluginDir, arg + ext))
				try:
					del loadedPlugins[arg]
				except:
					self.handler.Print('w', "Plugin wasn\'t loaded, skipping unloading")
				self.handler.Print('s', "Plugin removed.\n")
			except:
				self.handler.Print('f', "Could not remove plugin.\n")
		else:
			self.handler.Print('w', "Aborted.\n")

	def reload(self, _type):
		'''
		Reload plugins in case of errors etc
		'''
		if _type == "plugins":
			loadedPlugins.clear()
			plugins = [x for x in os.listdir(self.pluginDir) if os.path.splitext(x)[1] in self.supported and "init" not in x and "template" not in x]
			self.handler.write("\n")
			self.handler.Print('i', "Found {} plugin(s)".format(len(plugins)))
			self.handler.Print('i', "Loading plugins...")
			for plugin in plugins:
				if os.path.splitext(plugin)[1] == '.py':
					try:
						name, t = os.path.splitext(plugin)
						module = getattr(__import__(name, fromlist=[name]), name)
						loadedPlugins[name] = module
					except Exception as e:
						self.handler.Print('f', "Could Not Load: %s" % name)
						self.handler.Print('c', str(e))
			self.handler.Print('s', "Loaded {} plugin(s)\n".format(len(loadedPlugins)))
		elif _type == "tools":
			self.handler.Print('i', "Loading tools...")
			categories = os.listdir(self.toolDir)
			numTools = 0
			for category in categories:
				toolNames = os.listdir(os.path.join(self.toolDir, category))
				for toolName in toolNames:
					tools = [x for x in os.listdir(os.path.join(self.toolDir, category, toolName)) if os.path.splitext(x)[1] in self.supported and "init" not in x and "template" not in x]
					numTools += 1
					for tool in tools:
						if os.path.splitext(tool)[1] == '.py':
							try:
								name, t = os.path.splitext(tool)
								module = getattr(__import__(name, fromlist=[name]), name)
								configPath = os.path.join(self.toolDir, category, toolName, "config.yaml")
								loadedTools[name] = [module, configPath]
							except Exception as e:
								self.handler.Print('f', "Could Not Load: %s" % name)
								self.handler.Print('c', str(e))
			self.handler.Print('i', "Found {} tool(s)".format(numTools))
			self.handler.Print('s', "Loaded {} tool(s)\n".format(len(loadedTools)))

	def loadNew(self, _type):
		'''
		Ignore previously loaded plugins and only load newly discovered ones
		'''
		if _type == "plugins":
			plugins = [x for x in os.listdir(self.pluginDir) if x.endswith(".py") and "init" not in x and "template" not in x and os.path.splitext(x)[0] not in loadedPlugins]
			new = 0
			if len(plugins) != 0:
				self.handler.write("\n")
				self.handler.Print('i', "Found {} new plugin(s)".format(len(plugins)))
				self.handler.Print('i', "Loading plugins...")
				for plugin in plugins:
					if os.path.splitext(plugin)[1] == '.py':
						try:
							name, t = os.path.splitext(plugin)
							module = getattr(__import__(name, fromlist=[name]), name)
							loadedPlugins[name] = module
							new += 1
						except Exception as e:
							self.handler.Print('f', "Could Not Load: %s" % name)
							self.handler.Print('c', str(e))
				self.handler.Print('s', "Loaded {} new plugin(s)\n".format(new))
			else:
				self.handler.Print('w', "No New Plugins Found!\n")
		else:
			categories = os.listdir(self.toolDir)
			new = 0
			for category in categories:
				toolNames = os.listdir(os.path.join(self.toolDir, category))
				for toolName in toolNames:
					tools = [x for x in os.listdir(os.path.join(self.toolDir, category, toolName)) if os.path.splitext(x)[1] in self.supported and \
					"init" not in x and "template" not in x and os.path.splitext(x)[0] not in loadedTools]
					if len(tools) != 0:
						for tool in tools:
							if os.path.splitext(tool)[1] == '.py':
								try:
									name, t = os.path.splitext(tool)
									module = getattr(__import__(name, fromlist=[name]), name)
									loadedTools[name] = module
									new += 1
								except Exception as e:
									self.handler.Print('f', "Could Not Load: %s" % name)
									self.handler.Print('c', str(e))
						self.handler.Print('s', "Loaded {} new tool(s)".format(new))
						return
					else:
						self.handler.Print('w', "No New Tools Found!\n")
						return

if __name__ == "__main__":
	manager = Manager("/home/ginsu/Desktop/Toolbox/IntentLimit")
	manager.createPlugin()
	manager.loadNew()
	manager.removePlugin()
	manager.reloadPlugins()
