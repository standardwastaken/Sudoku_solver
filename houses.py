class Coll: #x
	
	def __init__(self, x, coll):
		
		self.x = x
		self.cont = coll
	
	def __str__(self):
		
		output = [str(_) for _ in self.cont]
		
		return str(output)		

class Row:  #y
	
	def __init__(self, y, row):
		
		self.y = y
		self.cont =row
	
	def __str__(self):
		
		output = [str(_) for _ in self.cont]
		
		return str(output)

class Box:  #b
	
	def __init__(self, b, box):
		
		self.b =b
		self.cont =box

	def __str__(self):
		
		output = [str(_) for _ in self.cont]
		
		return str(output)