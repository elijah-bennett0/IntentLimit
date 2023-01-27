import os

print(os.listdir())
toDel = "testp"

valid = []
for file in os.listdir():
	if toDel in file:
		valid.append(file)

if len(valid) > 1:
	print("More than one file with this name exists: ")
	[print(x) for x in valid]

ext = input('Extension: ')
os.system('rm -rf {}'.format(toDel + ext))
