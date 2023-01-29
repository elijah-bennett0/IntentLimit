# -*- coding: utf-8 -*-
"""
@Description		: Contexting for IntentLimit
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 1.0
"""

### Imports
#from command import *
###

__all__ = ["CmdCtx", "ToolCtx"]

### Code
class CmdCtx:
	"""
	Contexting
	"""
	def __init__(self, name, type):
		self.setName(name)
		self.setType(type)

	def getName(self) -> str:
		return self.name

	def getType(self) -> str:
		return self.type

	def setName(self, name):
		self.name = name

	def setType(self, type):
		self.type = type

	def lookupCmd(self, name: str) -> "Returns a function reference":
		return getattr(self, "do_" + name.lower())

	def lookupCompFunc(self, name: str) -> "Returns a function reference":
		return getattr(self, "complete_" + name.lower())

	def lookupHelpFunc(self, name: str) -> "Returns a function reference":
		print(getattr(self, "help_" + name.lower()))

	def getNames(self) -> list:
		names = []
		classes = [self.__class__]
		while classes:
			aclass = classes.pop(0)
			if aclass.__bases:
				classes += list(aclass.__bases__)
			names += dir(aclass)
		return names

	def setPlugin(self, unused):
		pass

	def getActive(self) -> str:
		return self.getName()

	def getPlugins(self) -> list:
		return []

class ToolCtx(base):
	"""
	This takes ILCMD to bring in the core functionality of IL plus the context commands
	specified here.

	EX:
	- set
		Set a variable (defined in the config.yaml file for the tool)
	- back
		Return to the previous context
	- use
		Use a part of the tool (ex. exploits, backdoors, etc)
	"""

	"""
	Set Command
	"""
	def help_set(self):
		usage = ["set [param]",
			"Set A Program Parameter"]
		self.io.print_usage(usage)

	def do_set(self, arg):
		"""Set a Program Parameter"""
		# Make method to load parameters out of the config file here

	"""
	Back Command
	"""
	def help_back(self):
		usage = ["back",
			"Return To a Previous Context"]
		self.io.print_usage(usage)

	def do_back(self):
		"""Return To a Previous Context"""
		pass

	"""
	Use Command
	"""
	def help_use(self):
		usage = ["use [name]",
			"Use An Exploit Or Another Program In The Tool."]
		self.io.print_usage(usage)

	def do_use(self, arg):
		"""Use An Exploit Or Another Program In The Tool."""
		pass

###

if __name__ == "__main__":
	pass
