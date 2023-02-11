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

@Description 	: Useful Google dorks
@Author		: Ginsu
@Date		: 6/16/22
@Version	: 1.0
"""

### Imports

###

__all__ = ["dorker"]
### Code
def dorker(handler):
	print("Mini Google Dorker")
	print("------------------")
	print("(1) Pages linked to URL")
	print("(2) Pages related to URL")
	print("(3) Files of specified TYPE")
	print("(4) Phonebook listings of NAME")
	option = int(input("\nChoice: "))
	ops = {1:"link: ", 
	       2:"related: ",
	       3:"filetype: ",
               4:"phonebook: "}
	if option in range(1,3):
		url = input("URL: ")
		string = ops[option] + url
	elif option == 3:
		file = input("Filetype: ")
		string = ops[option] + file
	# Not gonna bother with exception handling, if u mess it up
	# ur dumb
	else:
		name = input("Name: ")
		string = ops[option] + name

	handler.Print('s', "Enter this string into Google:\n\t=> {}".format(string))
###
