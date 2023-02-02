"""
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
