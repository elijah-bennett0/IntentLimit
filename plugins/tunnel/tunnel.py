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

@Description 	: Simple tunneler
@Author		: Ginsu
@Date		: 6/16/22
@Version	: 1.0
"""

### Imports
import subprocess as sp
###

__all__ = ["tunnel"]

### Code
def tunnel():
	print("Mini Simple Tunneler")
	print("--------------------")
	lport = input("Port to listen on: ")
	ip = input("IP to forward to: ")
	fport = input("Port to forward to: ")
	cmd = "socat TCP4:LISTEN:{} TCP:{}:{}".format(lport, ip, fport)
	sp.call(cmd, shell=True)
###

if __name__ == "__main__":
	tunnel()
