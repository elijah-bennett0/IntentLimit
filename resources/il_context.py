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

### Importsa
#from command import ILCMD : cant do due to circular import
import os
import cmd
import importlib
import subprocess as sp
from pathlib import Path
from integrityCheck import *
###

__all__ = ["CmdCtx", "ToolCtx", "PluginCtx"]

### Code
class CmdCtx(cmd.Cmd):
	"""
	Contexting
	"""
	def __init__(self, name, type):
		self.setName(name)
		self.setType(type)
		self.options = {}

	def getName(self):
		return self.name

	def getType(self):
		return self.type

	def setName(self, name):
		self.name = name

	def setType(self, type):
		self.type = type

	def lookupCmd(self, name):
		"""Returns a function reference"""
		return getattr(self, "do_" + name.lower())

	def lookupCompFunc(self, name):
		"""Returns a function reference"""
		return getattr(self, "complete_" + name.lower())

	def lookupHelpFunc(self, name):
		"""Returns a function reference"""
		return getattr(self, "help_" + name.lower())

	def getNames(self):
		names = []
		classes = [self.__class__]
		while classes:
			aclass = classes.pop(0)
			if aclass.__bases__:
				classes += list(aclass.__bases__)
			names += dir(aclass)
		return names

	def setPlugin(self, func, *args):
		self.plugin = func(*args)

	def getActive(self):
		return self.getName()

	def getPlugins(self):
		return self.plugin

	def loadTool(self, config, ILCMD): # returns a dynamic class for the loaded tool
		cfg = readConfig(config)

		command_specs = cfg["commands"]
		path = Path(os.path.dirname(os.path.abspath(config)) + "/coldheart.py") # path to main tool py file
		rel = path.with_suffix("").relative_to(self.baseDir)
		module = ".".join(rel.parts)
		handler = importlib.import_module(module) # uses dotted names not paths

		attrs = {}
		for cmd_name, cmd_info in command_specs.items():
			func = getattr(handler, cmd_name)
			attrs[f"do_{cmd_name}"] = func # {"do_test":<func test>}

		attrs["CMD_SPECS"] = command_specs
		ToolClass = type(f"ToolCtx_{cfg['name']}", (ToolCtx, ILCMD), attrs)

		return ToolClass

	def TEST(self):
		pass

class ToolCtx(CmdCtx):
	"""
	This takes ILCMD to bring in the core functionality of IL plus the context commands
	specified here.

	** Tools will take control of IO and run themselves. No parameter
		setting like in a plugin

	- back
		Return to the previous context
	"""

	def __init__(self, *args):
		super().__init__(args[0], args[1])

	def do_set(self, arg):
		"""Set a specified parameter."""
		name, value = arg.split(' ') # could make more robust later
		self.options[name] = value
		print(self.options)

	def help_options(self):
		print("TEST")

	def do_options(self, arg):
		"""Show context specific commands and params."""
		specs = getattr(self.__class__, "CMD_SPECS", {})
		if not specs:
			self.handler.Print('w', "No options for this context!")
		for cmd_name, cmd_spec in specs.items():
			print(f"\nCommand: {cmd_name}")
			params = cmd_spec.get("params", {})
			if not params:
				continue

			for param_name, info in params.items():
				ptype = info.get("type", "str")
				required = "required" if info.get("required") else "optional"
				desc = info.get("desc", "")

				# main line for the param
				print(f"  Param: {param_name} ({ptype}, {required})")
				# optional description on its own indented line
				if desc:
					print(f"    Desc: {desc}\n")


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
	def getParams(self, args):
		params = {}
		self.configPath = os.path.join(self.plugDir, self.ctx.getActive().lower(), 'config.yaml')
		self.config = readConfig(self.configPath)
		for param in self.config['params']:
			params.update({param:'None'})

		if args[0] is None:
			pass
		else:
			if args[0] not in params:
				self.io.Print('f', "Invalid parameter!")
			else:
				params[args[0]] = args[1]
		return params

	def help_set(self):
		usage = ["set [param]",
			"Set A Plugin Parameter"]
		self.io.print_usage(usage)

	def do_set(self, argStr):
		"""Set a parameter within the selected plugin"""
		args = argStr.split(' ')
		# args[0] = parameter name
		# args[1] = parameter value
		if len(args) < 2:
			self.io.Print('f', "Not enough arguments!")
		else:
			if args[0] in self.params:
				self.params[args[0]] = args[1]
			else:
				self.params = self.getParams(args)
		#print(self.ctx.getActive()) #<<<< WORKS
		# now just need to get method to read required params from
		# config file and set up error handling.
		# EX: if args[0] not in configParams: error

	def help_options(self):
		usage = ["options",
			"Shows parameters and their values"]
		self.io.print_usage(usage)

	def do_options(self, arg):
		"""Show plugin parameters and their values"""
		if not hasattr(self, 'params'):
			self.params = self.getParams([None, None])
		for k,v in self.params.items():
			self.io.Print('i', f"{k:<15}{v:>5}")

	"""
	Run Command
	"""
	def help_run(self):
		usage = ["run [plugin]",
			"Run The Selected Plugin"]
		self.io.print_usage(usage)

	def do_run(self, arg):
		"""Run the selected plugin"""
		plugin = self.loadedPlugins[self.ctx.getName()]
		if 'perl ' not in plugin[1] and 'bash ' not in plugin[1]:
			func = plugin[0]
			func(self.io, self.params)
		else:
			# needa fix this garbage. temp workaround
			if plugin[1] == 'perl ':
				ext = '.pl'
				cmd = plugin[1] + ' ' + plugin[0] + ext
			elif plugin[1] == 'bash ':
				ext = '.sh'
				cmd = plugin[1] + plugin[0] + ext
			p = sp.getoutput(cmd) # replace with subprocess?
			print(p)
	#def do_test(self, arg):
	#	print("PLUGIN CONTEXT SUCCESS")

###

if __name__ == "__main__":
	pass
