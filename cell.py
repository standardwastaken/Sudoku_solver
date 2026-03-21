class Cell:
	def __init__(self, x, y):
		self.aname = f'x{x}y{y}'
		self.value = 0
		self.cand = 10*[True]
		self.x = x
		self.y = y
		boxx = x//3
		boxy = y//3
		self.b = boxx + boxy*3

	def __str__(self):
		return str(self.value)

	def cand_count(self):
		a = 0
		for i in self.cand[1::]:
			if i:
				a+=1
		return a