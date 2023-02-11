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

@Description 	: Packet capture techniques
@Author		: Ginsu, RTFM
@Date		: 6/15/22
@Version	: 1.0
"""

### Imports
import subprocess as sp
###

__all__ = ["pack_cap"]

### Code
def pack_cap():
	print("Mini packet capturer")
	print("-----------------------")
	print("Modes: (1) By portrange (2) By IP")
	mode = int(input("Mode: "))
	iface = input("Interface name: ")
	if mode == 1:
		ports = input("Range ex. 22-23 : ")
		cmd = "tcpdump -nvvX -s0 -i {} tcp portrange {}".format(iface, ports)
	elif mode == 2:
		ip = input("IP: ")
		cmd = "tcpdump -I {} -tttt dst {}".format(iface, ip)

	print("[*] Running plugin...")
	sp.call(cmd, shell=True)
###

if __name__ == "__main__":
	pack_cap()
