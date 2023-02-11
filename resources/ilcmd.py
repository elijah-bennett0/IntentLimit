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
class IntentLimit(ILCMD, ):
	"""
	Basic Command Loading And Handling
	"""
	def __init__(self, configFile: str, baseDir=None, plugDir=None, toolDir=None, stdin=None, stdout=None, stderr=None):

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
		config: dict = readConfig(configFile)
		self.configvars: dict = config # config vars not from setg
		checkAndLoad(config: dict, self.io: "iohandler class from iohandler.py", baseDir)
		# ^ only checks from IntentLimit config.yaml
		# in each tool, call this method again specifying its own config.yaml

		# More config and variable stuff
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
