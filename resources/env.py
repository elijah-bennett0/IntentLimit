# -*- coding: utf-8 -*-
"""
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

__all__ = ["resizeConsole", "setupCorePaths", "addPath", "supportsColors"]

### Code
def resizeConsole(r: int, c: int):
	ret = subprocess.call("printf '\e[8;%s;%st'" % (r, c), shell=True)
	del ret

def setupCorePaths(ildir: str) -> tuple:
	IL_FILE = os.path.realpath(ildir)
	IL_DIR = os.path.dirname(IL_FILE)
	return (IL_FILE, IL_DIR)

def addPath(dir):
	sys.path.append(dir)

def supportsColors() -> bool:
	# Not too in depth but it works enuff.. probably
	max_colors = int(subprocess.getoutput('tput colors'))
	if max_colors > 0:
		return True
	else:
		return False
###

if __name__ == "__main__":
	pass
