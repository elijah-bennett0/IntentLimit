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

@Description		: Environment Operations For IntentLimit
@Author			: Ginsu
@Date			: 6/22/22
@Version		: 2.0
"""

### Imports
import os
import sys
import subprocess
###

__all__ = ["resizeConsole", "setupCorePaths", "addPath", "supportsColors", "addToolDirs", "addPluginDirs"]

### Code
def resizeConsole(r, c):
	ret = subprocess.call("printf '\e[8;%s;%st'" % (r, c), shell=True)
	del ret

def setupCorePaths(ildir):
	IL_FILE = os.path.realpath(ildir)
	IL_DIR = os.path.dirname(IL_FILE)
	return (IL_FILE, IL_DIR)

def addPath(dir):
	sys.path.append(dir)

def addPluginDirs(dir):
	for name in os.listdir(dir):
		addPath(os.path.join(dir, name))

def addToolDirs(dir):
	for cat in os.listdir(dir):
		for tool in os.listdir(os.path.join(dir, cat)):
			addPath(os.path.join(dir, cat, tool))

def supportsColors():
	# Not too in depth but it works enuff.. probably
	max_colors = int(subprocess.getoutput('tput colors'))
	if max_colors > 0:
		return True
	else:
		return False
###

if __name__ == "__main__":
	pass
