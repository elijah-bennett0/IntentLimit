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
import types
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
		tool_dir = Path(os.path.dirname(os.path.abspath(config)))
		tool_name = tool_dir.name.lower()
		path = tool_dir / f"{tool_name}.py"
		rel = path.with_suffix("").relative_to(self.baseDir)
		module = ".".join(rel.parts)
		handler = importlib.import_module(module) # uses dotted names not paths

		attrs = {}
		try:
			for cmd_name, cmd_info in command_specs.items():
				func = getattr(handler, cmd_name)
				attrs[f"do_{cmd_name}"] = func # {"do_test":<func test>}

			attrs["CMD_SPECS"] = command_specs
			attrs["TOOL_DIR"] = str(tool_dir)
			attrs["EXPLOITS_DIR"] = str(tool_dir / "exploits")
		except:
			self.io.Print('f', "No commands found for tool.")

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
		if not hasattr(self, "options"):
			self.options = {}
		args = arg.strip().split(None, 1)
		if len(args) < 2:
			self.io.Print('f', "Not enough arguments!")
			return
		name, value = args
		if name == "exploit":
			cve_name, cve_config = self.get_selected_cve_config(value)
			if cve_name and cve_config is None:
				self.io.Print('f', f"Unknown CVE for this tool: {cve_name}")
				return
			value = cve_name
		self.options[name] = value
		if name == "exploit" and value:
			self.io.Print('i', f"Selected {value}. Run options to view CVE-specific params.")
		#print(self.options)

	def normalize_cve_name(self, name):
		value = str(name or "").strip().lower().replace("-", "_")
		if value.startswith("cve_"):
			return value
		if value.startswith("cve"):
			return "cve_" + value[3:].lstrip("_")
		return value

	def get_selected_cve_config(self, cve_name=None):
		options = getattr(self, "options", {})
		cve_name = self.normalize_cve_name(cve_name or options.get("exploit"))
		if not cve_name:
			return None, None

		exploits_dir = getattr(self.__class__, "EXPLOITS_DIR", None)
		if not exploits_dir:
			return cve_name, None

		cfg_path = Path(exploits_dir) / cve_name / "config.yaml"
		if not cfg_path.exists():
			return cve_name, None

		return cve_name, readConfig(str(cfg_path))

	def help_options(self):
		print("TEST")

	def do_options(self, arg):
		"""Show context specific commands and params."""
		if not hasattr(self, "options"):
			self.options = {}
		cve_name, cve_config = self.get_selected_cve_config()
		if cve_name and cve_config:
			specs = cve_config.get("commands", {})
		else:
			specs = getattr(self.__class__, "CMD_SPECS", {})
		if not specs:
			self.io.Print('w', "No options for this context!")
			return

		if cve_name and cve_config:
			print(f"\n{self.getContext().getName()} selected CVE: {cve_name}\n")
			print("Commands:")
			for cmd_name, cmd_spec in specs.items():
				enabled = cmd_spec.get("enabled")
				if enabled is False:
					print(f"  {cmd_name} (disabled)")
				else:
					print(f"  {cmd_name}")
			print()

			params = {}
			for cmd_spec in specs.values():
				for param_name, info in cmd_spec.get("params", {}).items():
					params.setdefault(param_name, info)

			if not params:
				return

			required_params = {
				name: info for name, info in params.items()
				if info.get("required")
			}
			optional_params = {
				name: info for name, info in params.items()
				if not info.get("required")
			}

			for label, group in (("Required", required_params), ("Optional", optional_params)):
				if not group:
					continue
				print(f"{label}:")
				name_width = max(len(name) for name in group)
				for param_name, info in group.items():
					desc = info.get("desc") or info.get("type", "str")
					opts = info.get("opts") if info.get("opts") else None
					if opts:
						desc = f"{desc} Options: {opts}"
					current = self.options.get(param_name)
					default = info.get("default") if "default" in info else None
					if current is not None:
						desc = f"{desc} Current: {current}"
					elif default is not None:
						desc = f"{desc} Default: {default}"
					print(f"  {param_name:<{name_width}}  {desc}")
				print()
			return
		elif cve_name:
			self.io.Print('w', f"Selected CVE config not found: {cve_name}")
			print(f"\n{self.getContext().getName()} commands\n")
		else:
			print(f"\n{self.getContext().getName()} commands\n")
		seen_param_sets = {}
		for cmd_name, cmd_spec in specs.items():
			print(cmd_name)

			doc = getattr(getattr(self, f"do_{cmd_name}", None), "__doc__", "")
			if doc:
				print(f"  {doc.strip()}")

			params = cmd_spec.get("params", {})
			if not params:
				print()
				continue

			param_key = tuple(
				(param_name, repr(info or {}))
				for param_name, info in params.items()
			)
			if param_key in seen_param_sets:
				print(f"  Same parameters as {seen_param_sets[param_key]}.\n")
				continue
			seen_param_sets[param_key] = cmd_name

			required_params = {
				name: info for name, info in params.items()
				if info.get("required")
			}
			optional_params = {
				name: info for name, info in params.items()
				if not info.get("required")
			}

			for label, group in (("Required", required_params), ("Optional", optional_params)):
				if not group:
					continue
				print(f"  {label}:")
				name_width = max(len(name) for name in group)
				for param_name, info in group.items():
					desc = info.get("desc") or info.get("type", "str")
					opts = info.get("opts") if info.get("opts") else None
					if opts:
						desc = f"{desc} Options: {opts}"
					current = self.options.get(param_name)
					default = info.get("default") if "default" in info else None
					if current is not None:
						desc = f"{desc} Current: {current}"
					elif default is not None:
						desc = f"{desc} Default: {default}"
					print(f"    {param_name:<{name_width}}  {desc}")
				print()


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
		args = argStr.strip().split(None, 1)

		if len(args) < 2:
			self.io.Print('f', "Not enough arguments!")
			return

		name, value = args[0], args[1]

		if not hasattr(self, 'params'):
			self.params = self.getParams([None, None])

		if name not in self.params:
			self.io.Print('f', "Invalid parameter!")
			return

		self.params[name] = value
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
		plugin = self.loadedPlugins[self.ctx.getName().lower()]
		if type(plugin[0]) == types.FunctionType:
			func = plugin[0]
			if hasattr(self, 'params'):
				func(self.io, self.params)
			else:
				func(self.io)
		else:
			# needa fix this garbage. temp workaround
			print(plugin[0])
			if plugin[0] == 'perl ':
				ext = '.pl'
				cmd = plugin[0] + ' ' + self.ctx.getName().lower() + ext
			elif plugin[1] == 'bash ':
				ext = '.sh'
				cmd = plugin[0] + ' ' + self.ctx.getName().lower() + ext
			p = sp.getoutput(cmd) # replace with subprocess?
			print(p)
	#def do_test(self, arg):
	#	print("PLUGIN CONTEXT SUCCESS")

###

if __name__ == "__main__":
	pass
