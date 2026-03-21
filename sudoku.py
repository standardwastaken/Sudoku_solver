#udelat nejakej .md soubor na poznamky 
from cell import Cell
from houses import Coll, Row, Box
from copy import deepcopy

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
	
	def __str__(self): #TODO odebrat? (i v Cell a Houses)
		output =  [str(_) for _ in self.rows]
		tisk = ''
		for i in output:
			tisk+=i+'\n'
		return tisk
	
	def vloz_zadani(self, zadani=0): #TODO mozna smazat pozdeji #TODO rename to import()
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

	def export(self):
		export = self.grid.copy()
		for y in range(9):
			for x in range(9):
				export[y][x] = self.grid[y][x].copy()

	def val(self,x,y,value): #set value of a cell
		
		cell = self.grid[y][x]
		#check if value is valid
		if not self.possible(cell,value):
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
	
	def contains(self, type, coordinate, value): #check if a value is in a container #TODO dat do possible(), pokud to nebude pouzivat nikdo jinej
		if value==0:
			return False
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
	
	def possible(self, cell, value): #check if value is possible
		if self.contains("coll",cell.x, value):
			return False
		elif self.contains("row",cell.y, value):
			return False
		elif self.contains("box",cell.b, value):
			return False
		else:
			return True
	
	def solved(self): #returns 0 if unsolved, 1 if full, 2 if full and solved #TODO
		return 0

	def backtrack(self,solution_count=0): #bruteforce
		if solution_count>2:
			return solution_count
		global done; done = False
		for y in range(9):
			for x in range(9):
				if self.grid[y][x].value == 0:
					for i in range(1,10):
						if self.grid[y][x].cand[i] and self.possible(self.grid[y][x],i):
							self.grid[y][x].value = i
							output = self.backtrack(solution_count)
							if isinstance(output,int):
								solution_count = output
							else:
								solution_count=1
							if done ==True:
								done = False
								print(f'zvedam {solution_count}')
								solution_count+=1
								global solution
								solution = deepcopy(self)
							self.grid[y][x].value = 0
					if solution_count ==1:
						return solution
					return solution_count
		done =True
		return solution_count
	
	def nakedsingle(self): #if cell has only one candidate, make it its value
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
	def hiddensingle(self): #if value is possilble only in one place in a house, make it its value #TODO upravit podle hidden pairs etc
		for coll in self.colls:
			for i in range(1,10):
				solution = None
				for cell in coll.cont:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[i] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[i]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		for row in self.rows:
			for i in range(1,10):
				solution = None
				for cell in row.cont:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[i] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[i]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		for box in self.boxes:
			for i in range(1,10):
				solution = None
				for cell in box.cont:
					if cell.value == i:
						break
					elif cell.value ==0 and cell.cand[i] and solution == None:
						solution = cell
					elif cell.value ==0 and cell.cand[i]:
						solution = None
						break
				if solution != None:
					self.val(solution.x,solution.y,i)
					return True
		return False

'''Board=Sudoku()		
Board.vloz_zadani([['8', '0', '7', '0', '0', '0', '0', '0', '0'],
					['0', '3', '1', '0', '0', '2', '4', '0', '0'],
					['0', '4', '0', '0', '0', '0', '0', '5', '2'],
					['9', '6', '0', '4', '1', '0', '8', '7', '0'],
					['1', '0', '0', '7', '0', '3', '9', '2', '0'],
					['0', '0', '4', '9', '0', '8', '1', '0', '0'],
					['4', '0', '6', '1', '0', '7', '2', '3', '0'],
					['7', '5', '3', '0', '0', '0', '0', '9', '1'],
					['0', '1', '0', '0', '0', '6', '5', '0', '0']])
Board.backtrack(0)'''




