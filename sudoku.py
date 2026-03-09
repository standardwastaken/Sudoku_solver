#https://sudoku.com/
#gui
#vsechny fce asi rvat do class Sudoku
#nepouzivat exec()
#udelat nejakej .md soubor na poznamky 
#todo? #udělat cand z [1,3,4,9]  něco jako [True, False, True, True, False, False, False, False, True]


class Cell:
	def __init__(self, x, y):
		self.aname = f'x{x}y{y}'
		self.value = None
		self.cand = [1,2,3,4,5,6,7,8,9]
		self.x = x
		self.y = y
		boxx = x//3
		boxy = y//3
		self.b = boxx + boxy*3


	def __str__(self):
		return str(self.value)
		#return f'x{self.x}y{self.y}'
	def __repr__(self):
		return str(self)
#containers
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

class Sudoku:
	def __init__(self):
		#grid
		emptyrow = 9*[None]
		self.grid =9*[None]
		for i in range(9):
			self.grid[i] = emptyrow.copy()
		for yi in range(9):
			for xi in range(9):
				self.grid[yi][xi] = Cell(xi, yi)
		#row (y)
		self.rows = 9*[None]
		for yi in range(9):
			row =self.grid[yi]
			self.rows[yi] = Row(yi, row)
		#coll (x)
		self.colls = 9*[None]
		for xi in range(9):
			coll = 9*[None]
			for yi in range(9):
				coll[yi] = self.grid[yi][xi]
			self.colls[xi] = Coll(xi, coll)
		#box (b)
		self.boxes = 9*[None]
		for bi in range(9):
			lhx = (bi%3)*3    #levy horni x
			lhy = (bi//3)*3   #levy horni y
			box = 9*[None]
			boxi = 0
			for yi in range(lhy, lhy+3):
				for xi in range(lhx, lhx+3):
					box[boxi] = self.grid[yi][xi]
					boxi+=1
			self.boxes[bi] = Box(bi,box)
	def __str__(self):
		output =  [str(_) for _ in self.rows]
		tisk = ''
		for i in output:
			tisk+=i+'\n'
		return tisk
	def vloz_zadani(self):
		for y in range(9):
			input_row = input()
			if len(input_row) == 17:
				input_row = input_row.split()
			elif len(input_row) == 9:
				pass
			else:
				raise Exception.Invalid_zadani
			for x in range(len(input_row)):
				if input_row[x] != "0":
					self.val(x,y,int(input_row[x]))

	def val(self,x,y,value): #set value of a cell
		#check if value is valid
		try:
			intvalue =int(value)
		except:
			raise Exception.Value_error.invalid_value
		if value > 9 or value <1:
			raise Exception.Value_error.invalid_value
		#check if move is legal
		cell = self.grid[y][x]
		if self.contains('coll',cell.x,intvalue) or self.contains('row',cell.y,intvalue) or self.contains('box',cell.b,intvalue):
			raise Exception.Value_error.illigal_move
		#set value
		cell.value = value
		cell.cand = None
		#todo remove invalid candidates
		for xcell in self.colls[x].cont:
			if xcell.value == None:
				try:
					xcell.cand.remove(value)
				except ValueError:
					pass
		for ycell in self.rows[y].cont:
			if ycell.value == None:
				try:
					ycell.cand.remove(value)
				except ValueError:
					pass
		for bcell in self.boxes[cell.b].cont:
			if bcell.value == None:
				try:
					bcell.cand.remove(value)
				except ValueError:
					pass
	
	def contains(self, type, coordinate, value): #check if a value is in a container
		if coordinate<0 or coordinate>8:
			raise Exception.Invalid_coordinate
		if type == 'coll':
			for i in self.colls[coordinate].cont:
				if i.value ==value:
					return True
			return False
		elif type == 'row':
			for i in self.rows[coordinate].cont:
				if i.value ==value:
					return True
			return False
		elif type == 'box':
			for i in self.boxes[coordinate].cont:
				if i.value ==value:
					return True
			return False
		else:
			raise Exception.Type_error.unknown_type
	
	def possible(self, cell, value):
		if self.contains("coll",cell.x, value):
			return False
		elif self.contains("row",cell.y, value):
			return False
		elif self.contains("box",cell.b, value):
			return False
		else:
			return True
	
	def backtrack(self): #todo? #kinda incompatible s candidates
		global done; done = False
		for y in range(9):
			for x in range(9):
				if self.grid[y][x].value == None:
					for value in self.grid[y][x].cand:
						if self.possible(self.grid[y][x],value):
							self.grid[y][x].value = value
							self.backtrack()
							if done:
								return
							self.grid[y][x].value = None
					return		
		done = True
	
	def nakedsingle(self): #if cell has only one candidate, make it its vallue
		for y in range(9):
			for x in range(9):
				if self.grid[y][x].value == None:
					if len(self.grid[y][x].cand) == 1:
						self.val(x,y,self.grid[y][x].cand[0])
						return True
					elif len(self.grid[y][x].cand) == 0:
						raise Exception.Invalid_puzzle
		return False
	def hiddensingle(self): #todo #if value is possilble only in one place in container, place it there
		pass
	
	
	
	
	
	def main(self):#solvne cely sudoku, postupne v loopu vola dílčí fce
		board.vloz_zadani()
		print("jdu na to")
		while True:
			if self.nakedsingle():
				pass
			else:
				break
		print(board)
		print("backtrackin")
		board.backtrack()
		print(board)

board = Sudoku()
board.main()


