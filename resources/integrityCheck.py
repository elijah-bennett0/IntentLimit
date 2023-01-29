'''
Check the integrity of the program at specified PATH.
Author: Ginsu
Date: 6/30/22
Version: 2.0
'''
### Imports
import os
import yaml
from iohandler import *
###

__all__ = ["readConfig", "checkAndLoad"]

def readConfig(config: str) -> dict:
	with open(config) as file:
		try:
			_config = yaml.safe_load(file)
		except yaml.YAMLError as e:
			print(e)
	return _config

def checkAndLoad(config: dict, iohandler: "iohandler class from iohandler.py", PATH: str):
	# Should probably try to optimize this a bit

	missing = []
	dirs = config['default_dirs']
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
