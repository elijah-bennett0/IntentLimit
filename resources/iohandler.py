# -*- coding: utf-8 -*-
"""
@Description		: User IO Handling
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 1.0
"""

### Imports
import sys
###

__all__ = ["IOhandler", "truncate", "iowrap"]

### Code
def truncate(string, length):
    return string if (len(string) <= length) else ("%s... (plus %d characters)" % (string[:length], len(string) - length))

class IOhandler:
	"""
	Class to handle user IO
	"""
	def __init__(self, stdin=None, stdout=None):
		import sys
		if stdin is not None:
			self.stdin = stdin
		else:
			self.stdin = sys.stdin
		if stdout is not None:
			self.stdout = stdout
		else:
			self.stdout = sys.stdout

		self.stderr = self.stdout

		self.prefix = "\033["
		self.reset = f"{self.prefix}0m"
		self.highlight = f"{self.prefix}7m"
		self.red = f"{self.prefix}31m"
		self.green = f"{self.prefix}32m"
		self.yellow = f"{self.prefix}33m"
		self.blue = f"{self.prefix}34m"

		self.colormap = {
		"f":{"[-]":self.red,"attr":None},
		"s":{"[+]":self.green,"attr":None},
		"w":{"[!]":self.yellow,"attr":None},
		"i":{"[*]":self.blue,"attr":None},
		"c":{"[CRITICAL]":self.red,"attr":self.highlight}}

	def get_cmap(self):
		return self.colormap

	def write(self, text):
		self.stdout.write(text)

	def Print(self, type, text):
		colored = ""
		keys, values = list(self.colormap[type].keys()), list(self.colormap[type].values())
		pat, col, attr = keys[0], values[0], values[1]
		plen = len(pat)

		if attr:
			colored += col + attr + pat + self.reset
		else:
			for char in pat:
				if pat.find(char) == 1:
					colored += col + char + self.reset
				else:
					colored += char

		line = colored + " " + text + "\n"
		self.write(line)

	def print_usage(self, arg):
		self.write("Usage: \n\t%s\nDescription:\n\t%s\n" % (arg[0], arg[1]))

	def print_cmd_list(self, args):
		cmds = args['commands']
		for cmd in cmds:
			#print(cmd)
			cmdStr = "{:10}: {:30}\n".format(cmd[0], cmd[1])
			self.write(cmdStr)
def iowrap(func):
	def inner():
		handler = IOhandler()
		colormap = handler.get_cmap()
		out = func()
		status, msg = out.values()
		pat = list(colormap[status].keys())[0]
		col = list(colormap[status].values())[0]
		colpat = pat[0]+col+pat[1]+'\033[0m'+pat[2]
		sys.stdout.write(colpat+' '+msg+'\n')

	return inner

###

if __name__ == "__main__":
	handler = IOhandler()
	handler.Print('f', "Test")
	handler.Print('s', "Test")
	handler.Print('w', "Test")
	handler.Print('i', "Test")
	handler.Print('c', "Test")
