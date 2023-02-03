# -*- coding: utf-8 -*-

"""
@Description		: IntentLimit override for Python CMD
@Author			: Ginsu
@Date			: 20230201
@Version		: 2.3
"""

### Imports
import os
import cmd
import string
import subprocess
from context import *
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
		self.manager = Manager(baseDir=baseDir, plugDir=plugDir, toolDir=toolDir)
		self.promptpre = PROMPT_PRE
		self.setContext(None, None)

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

	def setContext(self, newCtx, Class):
		if newCtx is None:
			newCtx = self.defaultContext
		self.ctx = newCtx
		if Class:
			# Gotta love the amount of non-pythonic shit im doin here
			self.__class__ = type('ToolCtx',(ILCMD, Class),{})
		else:
			self.__class__ = type('ILCMD',(ILCMD,),{})
		self.setPrompt()

	def getContext(self):
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
			func, path = loadedPlugins[arg][0], loadedPlugins[arg][1]
			config = readConfig(os.path.join(self.plugDir,arg,"config.yaml"))
			self.setContext(CmdCtx(config['name'],config['type']), PluginCtx)
			self.__class__ = type('PluginCtx',(ILCMD,PluginCtx),{})
			print(func)
			func(self.io)
		elif arg in loadedTools:
			func, path = loadedTools[arg][0], loadedTools[arg][1]
			config = readConfig(path)
			self.setContext(CmdCtx(config['name'],config['type']), ToolCtx)
			func()
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
	def get_help_lists(self, names, ctx):
		do_cmds = list(set([name for name in names if name.startswith("do_")]))
		do_cmds.sort()
		return [(name[3:], str(getattr(ctx, name).__doc__)) for name in do_cmds]

	def do_help(self, input):
		"""Print Help"""
		args = input.strip().split()
		if len(args) > 0:
			arg = args[0]
			try:
				func = self.ctx.lookupHelpFunction(arg)
				func()
			except AttributeError:
				pass
			try:
				func = getattr(self, "help_" + arg.lower())
				func()
			except AttributeError:
				pass
		else:
			cmds = self.get_help_lists(self.get_names(), self)
			cmdlist = {"title":"Core Commands","commands":cmds}
			self.io.print_cmd_list(cmdlist)

			if self.ctx.getName() != self.defaultContext.getName():
				cmds = self.get_help_lists(self.ctx.getNames(), self.ctx)
				cmdlist = {"title":"%s Commands"%self.ctx.getType(),"commands":cmds}
				self.io.print_cmd_list(cmdlist)

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
			self.io.Print('f', "Info doesn't support plugins yet.")
		elif name not in loadedPlugins and name not in loadedTools and name != '':
			self.io.Print('f', "Couldn't find info about {}".format(name))
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
		if cmd is None:
			return self.default(line)
		if cmd == '':
			return self.default(line)
		else:
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


