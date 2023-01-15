"""
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
