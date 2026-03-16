#https://sudoku.com/
#udelat nejakej .md soubor na poznamky 

from cell import Cell
from houses import Coll, Row, Box

class Sudoku:
	def __init__(self):
		#grid
		emptyrow = 9*[0]
		self.grid =9*[0]
		for i in range(9):
			self.grid[i] = emptyrow.copy()
		for yi in range(9):
			for xi in range(9):
				self.grid[yi][xi] = Cell(xi, yi)
		#row (y)
		self.rows = 9*[0]
		for yi in range(9):
			row =self.grid[yi]
			self.rows[yi] = Row(yi, row)
		#coll (x)
		self.colls = 9*[0]
		for xi in range(9):
			coll = 9*[0]
			for yi in range(9):
				coll[yi] = self.grid[yi][xi]
			self.colls[xi] = Coll(xi, coll)
		#box (b)
		self.boxes = 9*[0]
		for bi in range(9):
			lhx = (bi%3)*3    #levy horni x
			lhy = (bi//3)*3   #levy horni y
			box = 9*[0]
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
	
	def vloz_zadani(self, zadani=0):
		if zadani==0:
			pass
		elif zadani==1:
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
		else:
			if len(zadani)==9:
				for y in range(9):
					if len(zadani[y])==9:
						for x in range(9):
							if zadani[y][x] != "0":
								self.val(x,y,int(zadani[y][x]))
					else:
						raise Exception.Invalid_zadani
			else:
				raise Exception.Invalid_zadani

	def val(self,x,y,value): #set value of a cell
		
		cell = self.grid[y][x]
		value =int(value)
		#check if value is valid
		if value !=0 and (self.contains('coll',cell.x,value) or self.contains('row',cell.y,value) or self.contains('box',cell.b,value)):
			raise Exception('Value_error.illigal_move')
		oldvalue = cell.value
		cell.value = value
		cell.cand = 10*[True]
		for i in self.colls[cell.x].cont:
			cell.cand[i.value]= False
			i.cand[cell.value]= False
			if self.possible(i, oldvalue):
				i.cand[oldvalue] = True
		for i in self.rows[cell.y].cont:
			cell.cand[i.value]= False
			i.cand[cell.value]= False
			if self.possible(i, oldvalue):
				i.cand[oldvalue] = True
		for i in self.boxes[cell.b].cont:
			cell.cand[i.value]= False
			i.cand[cell.value]= False
			if self.possible(i, oldvalue):
				i.cand[oldvalue] = True
	
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
				if self.grid[y][x].value == 0:
					for i in range(1,10):
						if self.grid[y][x].cand[i] and self.possible(self.grid[y][x],i):
							self.grid[y][x].value = i
							self.backtrack()
							if done:
								return
							self.grid[y][x].value = 0
					return		
		done = True
	
	def nakedsingle(self): #if cell has only one candidate, make it its vallue
		for y in range(9):
			for x in range(9):
				if self.grid[y][x].value == 0:
					if self.grid[y][x].cand_count() == 1:
						for i in range(1,10):
							if self.grid[y][x].cand[i]:
								self.val(x,y,i)
						return True
					elif self.grid[y][x].cand_count() == 0:
						raise Exception('No solution')
		return False
	def hiddensingle(self): #todo #if value is possilble only in one place in container, place it there
		for coll in self.colls:
			for i in range(1,10):
				solution = None
				for cell in coll:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[True] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[True]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		for row in self.rows:
			for i in range(1,10):
				solution = None
				for cell in row:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[True] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[True]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		for box in self.boxes:
			for i in range(1,10):
				solution = None
				for cell in box:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[True] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[True]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		return False
		

	
	
	
	
	def main(self,zadani=0):#solvne cely sudoku, postupne v loopu vola dílčí fce
		self.vloz_zadani(zadani)
		print("jdu na to")
		while True:
			if self.nakedsingle():
				pass
			else:
				break
		self.backtrack()
		
Board = Sudoku()
Board.main([['0', '0', '0', '0', '2', '0', '6', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '7', '4'],
			['0', '0', '0', '9', '1', '0', '0', '0', '0'],
			['0', '2', '0', '0', '0', '0', '0', '0', '9'],
			['4', '1', '6', '0', '0', '0', '0', '0', '0'],
			['0', '9', '0', '4', '0', '0', '5', '0', '0'],
			['0', '0', '0', '0', '6', '0', '0', '5', '0'],
			['7', '0', '0', '1', '0', '2', '0', '0', '0'],
			['6', '0', '8', '0', '0', '0', '0', '3', '0']])



