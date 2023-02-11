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

@Description		: User IO Handling
@Author			: Ginsu
@Date			: 20230120
@Version		: 2.2
"""

### Imports
import sys
###

__all__ = ["IOhandler", "iowrap"]

### Code

class IOhandler():
	"""
	Class to handle user IO
	"""
	def __init__(self, enable_color, stdin=None, stdout=None):
		import sys
		if stdin is not None:
			self.stdin = stdin
		else:
			self.stdin = sys.stdin
		if stdout is not None:
			self.stdout = stdout
		else:
			self.stdout = sys.stdout

		self.enable_color = enable_color
		self.stderr = self.stdout

		self.prefix = "\033["
		self.reset = f"{self.prefix}0m"
		self.highlight = f"{self.prefix}7m"
		self.red = f"{self.prefix}31m"
		self.green = f"{self.prefix}32m"
		self.yellow = f"{self.prefix}33m"
		self.blue = f"{self.prefix}36m"
		self.magenta = f"{self.prefix}35m"

		self.stylemap = {
                "f":{"[-]":'',"attr":None},
                "s":{"[+]":'',"attr":None},
                "w":{"[!]":'',"attr":None},
                "i":{"[*]":'',"attr":None},
                "c":{"[CRITICAL]":'',"attr":self.highlight},
                "q":{"[?]":'',"attr":None}}

		self.colormap = {
		"f":{"[-]":self.red,"attr":None},
		"s":{"[+]":self.green,"attr":None},
		"w":{"[!]":self.yellow,"attr":None},
		"i":{"[*]":self.blue,"attr":None},
		"c":{"[CRITICAL]":self.red,"attr":self.highlight},
		"q":{"[?]":self.magenta,"attr":None}}

	def truncate(self, string: str, length: int) -> str:
		return string if (len(string) <= length) else ("%s... (plus %d characters)" % (string[:length], len(string) - length))

	def get_cmap(self, enable_color: bool) -> dict:
		if enable_color:
			return self.colormap
		else:
			return self.stylemap

	def write(self, text):
		self.stdout.write(text)

	def Print(self, type, text, *args):
		if self.enable_color:
			map = self.colormap
		else:
			map = self.stylemap
		colored = ""
		keys, values = list(map[type].keys()), list(map[type].values())
		pat, col, attr = keys[0], values[0], values[1]
		plen = len(pat)
		if len(args) == 0:
			end = '\n'
		else:
			end = args[0]

		if attr:
			colored += col + attr + pat + self.reset
		else:
			for char in pat:
				if pat.find(char) == 1:
					colored += col + char + self.reset
				else:
					colored += char

		line = colored + " " + text + end # Bug i think. *args might do weird shit
		self.write(line)

	def get_input(self, text: str) -> str:
		self.Print('q', text, '')
		i = input()
		return i

	def print_usage(self, arg):
		self.write("Usage: \n\t%s\nDescription:\n\t%s\n" % (arg[0], arg[1]))

	def print_cmd_list(self, args):
		cmds = args['commands']
		self.write("\n")
		for cmd in cmds:
			cmdStr = "  {:10}: {:30}\n".format(cmd[0], cmd[1])
			self.write(cmdStr)
		self.write("\n")

def iowrap(func):
	def inner():
		'''
		Very basic hacky coloring for plugins. Just needed it to work for now.
		Can fix in later update.
		'''
		handler = IOhandler(True)
		colormap = handler.get_cmap(True)
		out = func()
		status, msg = out.values()
		pat = list(colormap[status].keys())[0]
		col = list(colormap[status].values())[0]
		colpat = pat[0]+col+pat[1]+'\033[0m'+pat[2]
		sys.stdout.write(colpat+' '+msg+'\n')

	return inner

###

if __name__ == "__main__":
	handler = IOhandler(True) # True for colors, False for no color
	handler.Print('f', "Test")
	handler.Print('s', "Test")
	handler.Print('w', "Test")
	handler.Print('i', "Test")
	handler.Print('c', "Test")
	i = handler.get_input("Test > ")
