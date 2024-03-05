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

@Description		: Exception Handling Classes
@Author			: Ginsu
@Date			: 6/21/22
@Version		: 1.0
"""

### Imports
import sys
from iohandler import *
###

__all__ = ["Interpreter", "CmdErr", "PromptErr", "ExceptionWrapped"]

### Code
class CmdErr(Exception):
	"""
	Class for command errors
	"""
	def __init__(self, error):
		self.error = str(error)
		self.prefix = "Error:"
	def getErr(self):
		return "%s %s" % (self.prefix, self.error)

class PromptErr(CmdErr):
	"""
	Class for prompt errors
	"""
	def __init__(self, error):
		CmdErr.__init__(self, error)
		self.prefix = "Prompt Error:"

class Interpreter(Exception):
	"""
	Class for the interpreter exception
	"""
	def __init__(self):
		self.prefix = "Dropping to Interpreter"

	def getErr(self):
		return "%s" % self.prefix

def ExceptionWrapped(func):
	"""
	Decorator to catch unhandled error
	"""
	def wrap(*args, **kwargs):
		try:
			ret = func(*args, **kwargs)
			return ret
		except SystemExit:
			return None
		except:
			import traceback
			trace = traceback.format_exc()
			print(' '*37+"==========================", file=sys.stderr)
			print(' '*37+"=  Unhandled Exception:  =", file=sys.stderr)
			print(' '*37+"==========================", file=sys.stderr)
			print('\n'+"="*100+'\n', file=sys.stderr)
			print("%s" % (trace), file=sys.stderr)
			print('\n'+"="*100, file=sys.stderr)
			return None
		wrap.__doc__ = func.__doc__
	return wrap
###

if __name__ == "__main__":
	pass
