import subprocess

def debug(self, arg):
	'''Main debug command to use krakentrap'''

	# intentlimit handle for krakentrap. very basic stages
	subprocess.call(["./krakentrap", arg])
