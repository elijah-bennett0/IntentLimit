#-*- coding: utf-8 -*-
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

@Description		: IntentLimit override for Python CMD
@Author			: Ginsu
@Date			: 20230201
@Version		: 2.3
"""

### Imports
import re
import os
import cmd
import string
import subprocess
from typing import *
from il_context import CmdCtx, ToolCtx, PluginCtx
from iohandler import *
from exception import *
from pluginManager import *
from env import supportsColors
from integrityCheck import readConfig
###

__all__ = ["ILCMD"]

### Code
PROMPT_PRE = "(IL" # make prompt prettier; [IL:Exploitation\Coldheart] >   like this
PROMPT_POST = ") > "
PROMPT_FMTSTR = ":%s:%s"

class ILCMD(cmd.Cmd):
	"""
	IntentLimit override for Python CMD

	Overrides a few base commands of CMD
	- help
	- shell
	- quit
	- python
	"""

	identchars = string.ascii_letters + string.digits + '_'
	helpKeys = {'?': "help"}
	shortcutKeys = {'?': "help", '!': "shell"}

	def __init__(self, baseDir=None, plugDir=None, toolDir=None, stdin=None, stdout=None, stderr=None):
		self.baseDir, self.plugDir, self.toolDir, = baseDir, plugDir, toolDir
		self.init_io(supportsColors(), stdin=stdin, stdout=stdout, stderr=stdout)
		self.defaultContext = CmdCtx("IntentLimit", "IntentLimit")
		self.manager: ClassVar = Manager(baseDir=baseDir, plugDir=plugDir, toolDir=toolDir)
		self.promptpre = PROMPT_PRE
		self.setContext(None, None)

		self.loadedPlugins = loadedPlugins
		self.loadedTools = loadedTools

	"""
	IO Handling
	"""
	def init_io(self, colors, stdin=None, stdout=None, stderr=None):
		self.io = IOhandler(colors, stdin=stdin, stdout=stdout)

	"""
	Context/Prompt Operations
	"""
	def setPrompt(self, prompt=None):
		if prompt is None:
			if self.getContext().getName() == self.defaultContext.getName():
				context = ""
			else:
				context = PROMPT_FMTSTR % (self.getContext().getType(), self.getContext().getName())
			prompt = self.promptpre + context + PROMPT_POST
		self.prompt = prompt

	def setContext(self, newCtx, config):
		if newCtx is None:
			self.ctx = self.defaultContext
			self.__class__ = type('ILCMD',(ILCMD,),{}) #bug fix. needed to reset the __class__ from the previous context
		else:
			if newCtx[1].lower() == 'plugin':
				#c = CmdCtx(newCtx[0], newCtx[1])
				self.__class__ = type('PluginCtx',(ILCMD, PluginCtx),{})
				#self.__bases__ = (cmd.Cmd,ILCMD,CmdCtx)
				#else:
					#self.__class__ = type('ILCMD',(ILCMD,),{})
				self.ctx = PluginCtx(newCtx[0], newCtx[1])
			else: # tool context
				ToolClass = CmdCtx.loadTool(self, config, ILCMD)
				self.__class__ = ToolClass # dynamic named class to allow tool-specific commands
				self.ctx = ToolClass(newCtx[0], newCtx[1])
				#ToolClass.__init__(newCtx[0], newCtx[1])

		self.setPrompt()

	def getContext(self) -> "A CmdCtx instance from context.py":
		return self.ctx

	"""
	Loadnew Command
	"""
	def help_loadnew(self):
		usage = ["loadnew [plugins][tools]",
			"Load New Plugins Or Tools"]
		self.io.print_usage(usage)

	def do_loadnew(self, arg):
		"""Load New Plugins Or Tools"""
		if arg == "plugins":
			self.manager.loadNew("plugins")
		elif arg == "tools":
			self.manager.loadNew("tools")
		else:
			self.help_loadnew()

	"""
	Create Command
	"""
	def help_create(self):
		usage = ["create [name]",
			"Create A Plugin Template"]
		self.io.print_usage(usage)

	def do_create(self, arg):
		"""Create A Plugin Template"""
		if arg:
			self.manager.createPlugin(arg)
		else:
			self.help_create()

	"""
	Remove Command
	"""
	def help_remove(self):
		usage = ["remove [name]",
			"Removes A Specified Plugin"]
		self.io.print_usage(usage)

	def do_remove(self, arg):
		"""Removes A Specified Plugin"""
		if arg:
			self.manager.removePlugin(arg)
		else:
			self.help_remove()

	"""
	Reload Command
	"""
	def help_reload(self):
		usage = ["reload [plugins][tools]",
			"Reload Plugins Or Tools"]
		self.io.print_usage(usage)

	def do_reload(self, arg):
		"""Reload Plugins Or Tools"""
		if arg == "plugins":
			self.manager.reload("plugins")
		elif arg == "tools":
			self.manager.reload("tools")
		else:
			self.help_reload()

	"""
	Use Command
	"""
	def help_use(self):
		usage = ["use [name]",
			"Use A Specified Plugin Or Tool"]
		self.io.print_usage(usage)

	def do_use(self, arg):
		"""Use A Specified Plugin Or Tool"""
		if arg in loadedPlugins:
			if os.path.exists(loadedPlugins[arg][1]):
				func, path = loadedPlugins[arg][0], loadedPlugins[arg][1]
			else:
				pass
			config = readConfig(os.path.join(self.plugDir,arg,"config.yaml"))
			self.setContext((config['name'], config['type']), PluginCtx)
		elif arg in loadedTools:
			func, path = loadedTools[arg][0], loadedTools[arg][1]
			config = readConfig(path)
			self.setContext((config['name'], config['type']), path)
			#func()
		else:
			self.help_use()

	def help_back(self):
		usage = ["back",
			"Return to base context"]
		self.io.print_usage(usage)

	def do_back(self, arg):
		"""Return To Previous Context"""
		self.setContext(None, None)
		self.setPrompt()

	"""
	Show Command
	"""
	def help_show(self):
		usage = ["show [plugins][tools]",
			"Shows Loaded Tools Or Plugins"]
		self.io.print_usage(usage)

	def do_show(self, arg):
		"""Show Loaded Tools Or Plugins"""
		if arg == 'plugins':
			for p in loadedPlugins:
				self.io.Print('s', "Loaded: %s" % p)
		elif arg == 'tools':
			for t in loadedTools:
				self.io.Print('s', "Loaded: %s" % t)
		else:
			self.help_show()

	"""
	Shell Command
	"""
	def help_shell(self):
		usage = ["shell [command [args]]",
			"Runs command with args in OS shell"]
		self.io.print_usage(usage)

	def do_shell(self, arg):
		"""Execute CLI Command"""
		try:
			retcode = subprocess.call(arg, shell=True)
			del retcode
		except OSError(e):
			# Bug 3 (6/28/22): self.io.write changed to Print
			self.io.Print('f', "Failed: %s" % e.message)
		except KeyboardInterrupt:
			self.io.Print('w', "Aborted by user!")

	"""
	Quit Command
	"""
	def help_quit(self):
		usage = ["quit","Quits Program"]
		self.io.print_usage(usage)

	def do_quit(self, arg):
		"""Exit IntentLimit"""
		return True

	"""
	Bug 2: No EOF functionality, fixed here.
	"""
	def help_eof(self):
		usage = ["exit", "Exits Program (CTRL-D)"]
		self.io.print_usage(usage)

	def do_eof(self, arg):
		"""Exit IntentLimit (CTRL-D)"""
		return True

	"""
	Exit Command
	"""
	def help_exit(self):
		usage = ["exit", "Exits Program"]
		self.io.print_usage(usage)

	def do_exit(self, arg):
		"""Exit IntentLimit"""
		return True

	"""
	Python Command
	"""
	def help_python(self):
		usage = ["python",
			"Enter Python Interpreter"]
		self.io.print_usage(usage)

	def do_python(self, arg):
		"""Python Interpreter"""
		raise Interpreter

	"""
	Help Command
	"""
	def get_help_lists(self, names, ctx) -> list:
		do_cmds = sorted({name for name in names if name.startswith("do_")})
		out = []
		for name in do_cmds:
			try:
				obj = getattr(ctx, name)
				doc = obj.__doc__ or ""
			except:
				doc = ""
			out.append((name[3:], doc))
		return out

	def do_help(self, input):
		"""Print Help"""
		args = input.strip().split()
		if len(args) > 0:
			arg = args[0].lower()
			func = getattr(self, f"help_{arg}", None)
			if callable(func):
				return func()
			self.io.Print('f', f"No help available for '{arg}'")
			return
		else:
			self.io.Print('i', "Default Commands")
			core_names = dir(ILCMD)
			core_cmds = self.get_help_lists(core_names, ILCMD)
			self.io.print_cmd_list({"title":"Core Commands","commands":core_cmds})

			if self.ctx.getName() != self.defaultContext.getName():
				#print("NOT DEFAULT CONTEXT")
				#print(self.ctx)
				#print(self.ctx.getNames())
				#print(PluginCtx.__class__)
				self.io.Print('i', "Context Specific Commands")
				dyn_names = set(dir(self.__class__)) - set(dir(ILCMD))
				ctx_cmds = self.get_help_lists(sorted(dyn_names), self)
				#print("CMDS:",cmds)
				self.io.print_cmd_list({"title":"%s Commands"%self.ctx.getType(),"commands":ctx_cmds})

	"""
	Search Command
	"""
	def help_search(self):
		usage = ["search [term]",
			"Show related matches to a specified term"]
		self.io.print_usage(usage)

	def do_search(self, term):
		"""Show related matches to a specified term"""
		try:
			cfg = readConfig(self.baseDir + "/resources/database.yaml")
			tokens = [t.lower() for t in term.split() if t.strip()]
			if not tokens:
				self.help_search()
				return

			def norm(x):
				return str(x).lower().replace("_", " ").replace("-", " ")

			results = []
			for item in cfg.get("items", []):
				fields = [
					item.get("name", ""),
					item.get("kind", ""),
					item.get("category", ""),
					item.get("desc", ""),
					item.get("action", ""),
					" ".join(str(t) for t in item.get("tags", []) or []),
				]
				if all(norm(t) in norm(" ".join(fields)) for t in tokens):
					results.append(item)

			if not results:
				self.io.Print('f', f"No results for {term}")
				return

			self.io.Print('i', f"Search: {term}")
			self.io.Print('i', f"Matches: {len(results)}")
			print()
			print("    ID               Sev        Product              Summary")
			print("    ----------------------------------------------------------------------")

			for result in results[:50]:
				name = str(result.get("name", ""))[:16].ljust(16)
				desc = str(result.get("desc", "")).replace("\n", " ")
				sev = "INFO"
				for x in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
					if x.lower() in desc.lower():
						sev = x
						break

				product = "Unknown"
				for x in ("Apache Log4j", "Apache ActiveMQ", "Apache", "WordPress", "phpMyAdmin", "Tomcat", "Jenkins", "Drupal", "Fortinet", "Cisco"):
					if x.lower() in desc.lower():
						product = x
						break

				summary = desc.split(":", 1)[-1].strip()
				if len(summary) > 150:
					summary = summary[:97] + "..."

				self.io.Print('s', f"{name} {sev.ljust(10)} {product[:20].ljust(20)} {summary}")

			if len(results) > 50:
				self.io.Print('w', f"Showing 50 of {len(results)} results. Refine your search.")

			print()
			self.io.Print('i', "use <id>   info <id>")
			print()

		except Exception as e:
			self.io.Print('f', f"Something went wrong... report to author: {e}")

	def do_searchui(self, term):
		"""Planning to use ncurses and C to show a graphical UI searching function"""
		pass

	"""
	Info Command
	"""
	def help_info(self):
		usage = ["info [tool name][plugin name]",
			"Show relevant info about a tool or plugin"]
		self.io.print_usage(usage)

	def do_info(self, name):
		"""Show Information About A Tool Or Plugin"""
		if name in loadedTools:
			path = loadedTools[name][1]
			config = readConfig(path)
			self.io.Print('i', "{} version {} : {}".format(config['name'], config['version'], config['description']))
		elif name in loadedPlugins:
			path = loadedPlugins[name][1]
			config = readConfig(path)
			self.io.Print('i', "{} version {} : {}".format(config['name'], config['version'], config['description']))
		elif name not in loadedPlugins and name not in loadedTools and name != '' and name != 'list': # probably should clean this up
			found_any = False

			try:
				for tool_key, (func, cfg_path) in loadedTools.items():
					cfg = readConfig(cfg_path)
					for cmd, cmdspec in cfg.get("commands", {}).items():
						for param, pspec in cmdspec.get("params", {}).items():
							opts = pspec.get("opts")
							if not opts:
								continue
							if isinstance(opts, str):
								opt_list = [o.strip() for o in opts.split(",") if o.strip()]
							elif isinstance(opts, (list, tuple, set)):
								opt_list = [str(o).strip() for o in opts if str(o).strip()]
							else:
								continue

							if name in opt_list:
								found_any = True

								# Try to load touch config next to the tool config
								subcfg_path = os.path.join(os.path.dirname(cfg_path), "touches", name, "config.yaml")

								try:
									touch_cfg = readConfig(subcfg_path)
									self.io.Print(
										'i',
										"{} version {} : {}".format(
										touch_cfg.get("name", name),
										touch_cfg.get("version", "?"),
										touch_cfg.get("description", "(no description)"),
										)
									)
								except Exception:
									# fallback: at least explain where it was found
									self.io.Print('i', f"'{name}' is an option for {cfg.get('name', tool_key)}.{cmd} param '{param}' (no touch config at {subcfg_path})")
			except: # eh
				pass
			if not found_any:
				self.io.Print('f', f"Couldn't find info about {name}")
		elif name == "list":
			self.io.Print('n', "\n")
			self.io.Print('i', "Tool Information")
			for tool in loadedTools.keys():
				config = readConfig(loadedTools[tool][1])
				self.io.Print('s', "{:25} : {:50}".format(f"{config['name']} version {config['version']}", f"{config['description']}"))
			self.io.Print('n', "\n\n")
			self.io.Print('i', "Plugin Information")
			for plugin in loadedPlugins.keys():
				config = readConfig(loadedPlugins[plugin][1])
				self.io.Print('s', "{:25} : {:60}".format(f"{config['name']} version {config['version']}", f"{config['description']}"))
			self.io.Print('n', "\n")
		else:
			self.help_info()

	def parseLine(self, line):
		line = line.strip()
		if not line:
			return None, None, line
		if line[-1:] in self.helpKeys:
			line = self.helpKeys[line[-1:]] + " " + line[:-1]

		if line[0] in self.shortcutKeys:
			line = self.shortcutKeys[line[0]] + " " + line[1:]

		i, n = 0, len(line)
		while i < n and line[i] in self.identchars:
			i = i+1
		cmd, arg = line[:i], line[i:].strip()
		return cmd, arg, line

	def onecmd(self, line):
		cmd, arg, line = self.parseLine(line)
		if not line:
			return self.emptyline()
		if cmd is None or cmd == '':
			return self.default(line)
		try:
			func = self.ctx.lookupCmd(cmd)
			return func(arg)
		except AttributeError:
			try:
				func = getattr(self, "do_" + cmd.lower())
			except AttributeError:
				return self.default(line)
			return func(arg)


	def emptyline(self):
		pass

	def default(self, line):
		cmd, arg, line = self.parseLine(line)

		try:
			func = self.ctx.lookupCmd(cmd)
		except AttributeError:
			self.io.Print('f', "Unknown syntax: %s" % line)
		else:
			func(arg)
###

if __name__ == "__main__":
	il = ILCMD()
	il.cmdloop()


