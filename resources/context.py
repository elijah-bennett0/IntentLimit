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

@Description		: Contexting for IntentLimit
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 1.0
"""

### Imports
<<<<<<< HEAD
#from command import *
=======

>>>>>>> 8c930fa228ae948a3c4199c9385e472cc988d51a
###

__all__ = ["CmdCtx", "ToolCtx", "PluginCtx"]

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
			if aclass.__bases__:
				classes += list(aclass.__bases__)
			names += dir(aclass)
		return names

	def setPlugin(self, unused):
		pass

	def getActive(self) -> str:
		return self.getName()

	def getPlugins(self) -> list:
		return []

<<<<<<< HEAD
class ToolCtx(base):
=======
class ToolCtx(CmdCtx):
>>>>>>> 8c930fa228ae948a3c4199c9385e472cc988d51a
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
	- run
		Run the selected tool
	"""

	"""
	Set Command
	"""
	def help_set(self):
		usage = ["set [param]",
			"Set A Tool Parameter"]
		self.io.print_usage(usage)

	def do_set(self, arg):
		"""Set a Tool Parameter"""
		# Make method to load parameters in another script, import it and implement it here

	"""
	Use Command
	"""
	def help_use(self):
		usage = ["use [name]",
			"Use An Exploit Or Another Program In The Tool."]
		self.io.print_usage(usage)

	def do_use(self, arg):
		"""Use An Exploit Or Another Program In The Tool."""
		pass # WRITE USE METHOD FOR THE TOOLS INSIDE THE SUB-FRAMEWORKS (Ex. using eternalblue in ColdHeart)

	"""
	Run Command
	"""
	def help_run(self):
		usage = ["run",
			"Run The Selected Tool/Program"]

	def do_run(self):
		pass

	def do_test(self, arg):
		print("CONTEXT SUCCESS")

class PluginCtx(CmdCtx):
	"""
	This will add the base functionality of IL plus the plugin specific commands

	EX:
	- set
		Set a plugin variable
	- run
		Run the plugin
	"""

	"""
	Set Command
	"""
	def help_set(self):
		usage = ["set [param]",
			"Set A Plugin Parameter"]
		self.io.print_usage(usage)

	"""
	Run Command
	"""
	def help_run(self):
		usage = ["run",
			"Run The Selected Plugin"]
		self.io.print_usage(usage)

	def do_run(self):
		pass

###

if __name__ == "__main__":
	pass
