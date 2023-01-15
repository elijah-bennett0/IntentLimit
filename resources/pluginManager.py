# -*- coding: utf-8 -*-
"""
@Description		: Manages plug-in scripts from /plugins
@Author			: Ginsu
@Date			: 6/16/22
@Version		: 1.3
"""

### Imports
import os
from iohandler import *
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
		self.handler   = IOhandler()
		self.supported = {'.py':'', '.pl':'perl ', '.sh':'./'}

	def loadPlugins(self):
		plugins = [x for x in os.listdir(self.pluginDir) if os.path.splitext(x)[1] in self.supported and "init" not in x and "template" not in x]
		#self.handler.write("\n")
		self.handler.Print('i', "Found {} plugin(s)".format(len(plugins)))
		self.handler.Print('i', "Loading plugins...")
		for plugin in plugins:
			if os.path.splitext(plugin)[1] == '.py':
				try:
					name, t = os.path.splitext(plugin)
					#print(os.getcwd())
					module = getattr(__import__(name, fromlist=[name]), name)
					loadedPlugins[name] = module
				except Exception as e:

					self.handler.Print('f', "Could Not Load: %s" % name)
					self.handler.Print('c', str(e))
		self.handler.Print('s', "Loaded {} plugin(s)\n".format(len(loadedPlugins)))

	def loadTools(self):
		categories = os.listdir(self.toolDir)
		for category in categories:
			toolNames = os.listdir(os.path.join(self.toolDir, category))
			for toolName in toolNames:
				tools = [x for x in os.listdir(os.path.join(self.toolDir, category, toolName)) if os.path.splitext(x)[1] in self.supported and "init" not in x and "template" not in x]
				self.handler.Print('i', "Found {} tool(s)".format(len(toolNames)))
				self.handler.Print('i', "Loading tools...")
				for tool in tools:
					if os.path.splitext(tool)[1] == '.py':
						try:
							name, t = os.path.splitext(tool)
							#print(os.getcwd())
							module = getattr(__import__(name, fromlist=[name]), name)
							loadedTools[name] = module
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

		Bug 1 (6/28/22): Remove only removes python plugins. Need a way to get extension with only the filename
		'''
		yn = input("[?] Sure you want to delete? (y/n): ")
		if yn == 'y':
			try:
				os.system("rm {}/{}.py".format(self.pluginDir, arg)) # Bug 1
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
		else:
			pass # tools here

	def loadNew(self, _type):
		'''
		Ignore previously loaded plugins and only load newly discovered ones
		'''
		if _type == "plugins":
			plugins = [x for x in os.listdir(self.pluginDir) if x.endswith(".py") and "init" not in x and "template" not in x and os.path.splitext(x)[0] not in loadedPlugins]
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
						except Exception as e:
							self.handler.Print('f', "Could Not Load: %s" % name)
							self.handler.Print('c', str(e))
				self.handler.Print('s', "Loaded {} new plugin(s)\n".format(len(plugins)))
			else:
				self.handler.Print('w', "No New Plugins Found!\n")
		else:
			pass # tools here
###

if __name__ == "__main__":
	manager = Manager("/home/ginsu/Desktop/Toolbox/IntentLimit")
	manager.createPlugin()
	manager.loadNew()
	manager.removePlugin()
	manager.reloadPlugins()