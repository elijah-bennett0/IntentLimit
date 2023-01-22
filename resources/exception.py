# -*- coding: utf-8 -*-
"""
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
