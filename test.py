class main:


	def __init__(self, name, type):
		self.name = name
		self.type = type

	def getName(self):
		return self.name

class main2:

	def test(self):
		print("TESTSTES")

class child(main):

	def __init__(self):
		#self.name = name
		#self.type = type
		pass

	def test(self):
		print(main(None, None).name)

m = main('Bin_Analysis', 'Plugin')
c = child()

c.test()

print(c.__class__)
c.__class__ = type('main2',(main, main2),{})
print(c.__class__)
c.test()
