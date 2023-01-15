"""
@Description 	: Useful Google dorks
@Author		: Ginsu
@Date		: 6/16/22
@Version	: 1.0
"""

### Imports
from resources import IOhandler
###

__all__ = ["dorker"]
### Code
@iowrap
def dorker():
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

	stat, msg = 's', "Enter this string into Google:\n\t=> {}".format(string))
	return {'status':stat, 'msg':msg}
###

if __name__ == "__main__":
	dorker()
