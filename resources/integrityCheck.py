'''
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

Check the integrity of the program at specified PATH.
Author: Ginsu
Date: 6/30/22
Version: 2.0
'''
### Imports
import os
from iohandler import *
###

__all__ = ["readConfig", "checkAndLoad"]

def readConfig(config):

	try:
		import yaml
	except ImportError:
		iohandler.Print('f', "Dependency missing: yaml")
		return

	with open(config) as file:
		try:
			_config = yaml.safe_load(file)
		except yaml.YAMLError as e:
			print(e)
	return _config

def checkAndLoad(config, iohandler, PATH):
	# Should probably try to optimize this a bit

	missing = []
	dirs = config['default_dirs']
	deps = config['dependencies']
	for dep in deps:
		try:
			__import__(dep)
		except:
			iohandler.Print('f', "Dependency missing:", dep)
	for _type, _list in dirs.items():
		if type(_list) == dict:
			for name, files in _list.items():
				for file in files:
					filePath = os.path.join(PATH,_type, name, file)
					if not os.path.exists(filePath):
						# [len(PATH):] to only show the relevent path, dont wanna show too much
						missing.append(filePath[len(PATH):])
		else:
			for file in _list:
				filePath = os.path.join(PATH, _type, file)
				if not os.path.exists(filePath):
					missing.append(filePath[len(PATH):])

	if len(missing) == 0:
		iohandler.write("\n")
		iohandler.Print('s', "Integrity check passed.")
	else:
		for path in missing:
			iohandler.Print('c', "Missing: {}".format(path))

if __name__ == "__main__":
	checkIntegrity("/home/ginsu/Desktop/Toolbox/IntentLimit_v2/tools/exploitation/ColdHeart")
