# -*- coding: utf-8 -*-
"""
@Description		: Contexting for IntentLimit
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 1.0
"""

### Imports

###

__all__ = ["CmdCtx"]

### Code
class CmdCtx:
	"""
	Contexting
	"""
	def __init__(self, name, type):
		self.setName(name)
		self.setType(type)

	def getName(self):
		return self.name

	def getType(self):
		return self.type

	def setName(self, name):
		self.name = name

	def setType(self, type):
		self.type = type

	def lookupCmd(self, name):
		return getattr(self, "do_" + name.lower())

	def lookupCompFunc(self, name):
		return getattr(self, "complete_" + name.lower())

	def lookupHelpFunc(self, name):
		print(getattr(self, "help_" + name.lower()))

	def getNames(self):
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

	def getActive(self):
		return self.getName()

	def getPlugins(self):
		return []
###

if __name__ == "__main__":
	pass
