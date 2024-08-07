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

@Description 	: Basic Binary Analysis Tools
@Author		: Ginsu
@Date		: 6/25/22
@Version	: 1.0
"""

### Imports
import os
import subprocess as sp
from datetime import *
###

__all__ = ["bin_analysis"]

### Code
def bin_analysis(handler, params):
	name = str(datetime.now()) # with open file: write all outs
	binary = params["binpath"]
	# still need to setup log location via config.yaml
	log_loc = handler.get_input("LOG Location: ")
	print('\n')
	handler.Print('i', "Getting basic file info...\n")
	out1 = file(handler, binary)
	#print('='*80)
	print('\n')
	handler.Print('i', "Getting strings...\n")
	out2 = strings(handler, binary)
	#print('='*80)
	print('\n')
	out3, out4, out5 = objdump(handler, binary)
	print('\n')
	out6 = strace(handler, binary)
	# outputs being saved so we can write to log file...
	# a lot of commands are dumping garbage out
	log(handler, log_loc, out1, out2, out3, out4, out5, out6)

def file(handler, binary):
	out = sp.getoutput(['file %s'%binary])
	l = out.split(',')
	for line in l:
		out = line.split(' ')
		if len(out) < 2:
			handler.Print('s', ' '.join(out))
		else:
			nl = []
			for ea in out:
				if len(ea) > 25:
					nea = handler.truncate(ea, 25)
				else:
					nea = ea
				nl.append(nea)

			handler.Print('s', ' '.join(nl))
	return out

def strings(handler, binary):
	out = sp.getoutput(['strings %s'%binary])
	for line in out.split('\n'):
		handler.Print('s', "Found: %s"%line)

def objdump(handler, binary):
	"""
	asm: objdump -M intel --no-show-raw-insn --no-addresses -d [file]
	strings from data section: objdump -sj .data [file]
	strings from rodata section: objdump -sj .rodata [file]
	"""
	handler.Print('i', "Dumping assembly...\n")
	out1 = sp.getoutput(['objdump -M intel --no-show-raw-insn --no-addresses -d %s'%binary])
	for line in out1.split('\n'):
		handler.Print('s', line)
	print('\n')
	handler.Print('i', "Dumping .data strings...\n")
	out2 = sp.getoutput(['objdump -sj .data %s'%binary])
	for line in out2.split('\n'):
		handler.Print('s', line)
	print('\n')
	handler.Print('i', "Dumping .rodata strings...\n")
	out3 = sp.getoutput(['objdump -sj .rodata %s'%binary])
	for line in out3.split('\n'):
		handler.Print('s', line)
	return out1,out2,out3

def strace(handler, binary):
	handler.Print('i', "Dumping strace info (if installed)...PRESS ENTER\n")
	out = sp.getoutput(['strace %s'%binary])
	if "not found" in out:
		q = handler.get_input("strace not found, would you like to install? y/n: ")
		if 'y' in q:
			try:
				os.system('sudo apt install strace')
				handler.Print('i', "Done.")

			except:
				handler.Print('f', "Error installing, try running as root?")
		else:
			handler.Print('i', "Skipping strace...")
	else:
		for line in out.split('\n'):
			handler.Print('s', line)
		return out

def ltrace(handler, binary):
	# do more research
	# example command: ltrace -x "@libc.so.6" -o out1.txt ./executable
	# -x : choose which functions to trace
	# -o : output file (optional)
	#
	pass
def hexdump(handler, binary):
	pass
###
def log(handler, location, *args):
	# allow user to change logpath at plugin start?
	# store in config.yaml
	log = open(location+"/log-%s.txt"%datetime.now(), 'w+')
	for arg in args:
		if arg is None:
			pass
		else:
			for line in arg:
				log.write(line)
	log.close()
	handler.Print('i', "Output logged.")
