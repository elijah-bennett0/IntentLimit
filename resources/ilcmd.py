
# -*- coding: utf-8 -*-
"""
@Description		: IntentLimit Context Specific Command Handling
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 2.0
"""

### Imports
import os
from env import *
from banner import *
from command import *
from integrityCheck import *
###

__all__ = ["IntentLimit"]

### Code
class IntentLimit(ILCMD):
	"""
	Context Specific Command Handling
	"""
	def __init__(self, configFile, baseDir=None, plugDir=None, toolDir=None, stdin=None, stdout=None, stderr=None):

		# Command/IO Handling
		ILCMD.__init__(self, baseDir=baseDir, plugDir=plugDir, toolDir=toolDir, stdin=stdin, stdout=stdout, stderr=stderr)

		# Visuals
		os.system("clear")
		self.banner = getBanner(os.path.join(baseDir, "resources"))
		self.io.write(self.banner)
		resizeConsole(25, 100) # r: 25, c: 100 is default

		# Config stuff
		self.completekey = 'tab'
		self.cmdqueue = []
		config = readConfig(configFile)
		self.configvars = config # config vars not from setg
		checkAndLoad(config, self.io, baseDir)
		# ^ only checks from IntentLimit config.yaml
		# in each tool, call this method again specifying its own config.yaml

		# More config and variable stuff
		self.postConfig()
		self.ilgvars = {} # IL global vars from setg -> MOVE TO command.py

	def postConfig(self):
		try:
			self.name = self.configvars['name']
			self.version = self.configvars['version']
		except:
			self.name = "IntentLimit"
			self.version = "2.0"
		self.defaultContext.setName(self.name)
		self.defaultContext.setType(self.name)
###

if __name__ == "__main__":
	pass
