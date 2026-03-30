from cell import *
from houses import *
from copy import deepcopy
from exceptions import *

class Sudoku:
	
	def __init__(self):
		
		#grid
		
		emptyrow = 9*[0]
		self.grid =9*[0]
		for i in range(9):
			self.grid[i] = emptyrow.copy()
		
		for y in range(9):
			for x in range(9):
				self.grid[y][x] = Cell(x, y)

		#row (y)
		
		self.rows = 9*[0]
		for y in range(9):
			row =self.grid[y]
			self.rows[y] = Row(y, row)

		#coll (x)
		
		self.colls = 9*[0]
		for x in range(9):
			coll = 9*[0]
			for y in range(9):
				coll[y] = self.grid[y][x]
			self.colls[x] = Coll(x, coll)
		
		#box (b)
		
		self.boxes = 9*[0]
		
		for b in range(9):
			
			box_lux = (b%3)*3    #left upper x
			box_luy = (b//3)*3   #left upper y
			box = 9*[0]
			boxi = 0
			
			for y in range(box_luy, box_luy+3):
				for x in range(box_lux, box_lux+3):
					box[boxi] = self.grid[y][x]
					boxi+=1
			
			self.boxes[b] = Box(b,box)
	
	def __str__(self): 
		
		rows =  [str(_) for _ in self.rows]
		output = '' 
		
		for i in rows:
			output+=i+'\n'
		
		return output
	
	def import_list(self, grid): #imports grid from list of lists
		
		if len(grid)==9:
	
			for y in range(9):					
				if len(grid[y])==9:
					
					for x in range(9):
						if grid[y][x] != "0":
							self.val(x,y,int(grid[y][x]))
				
				else:
					raise Exception(InvalidInput) 
		
		else:
			raise Exception(InvalidInput)

	def import_input(self): #imports grid using input()
		
		for y in range(9):
				
				input_row = input()
				
				if len(input_row) == 17:
					input_row = input_row.split()
				
				elif len(input_row) == 9:
					pass
				
				else:
					raise Exception(InvalidInput)
				
				for x in range(len(input_row)):
					if input_row[x] != "0":
						self.val(x,y,int(input_row[x]))

	def val(self,x,y,value): #set value of a cell and updates all affected candidates
		
		cell = self.grid[y][x]
		
		#check if value is valid
		if not self.possible(cell,value):
			raise Exception(IlligalMove)
		
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
		
		if value==0:
			return False
		
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
	
	def possible(self, cell, value): #check if value is possible
		
		if self.contains("coll",cell.x, value):
			return False
		
		elif self.contains("row",cell.y, value):
			return False
		
		elif self.contains("box",cell.b, value):
			return False
		
		else:
			return True
	
	def solved(self): 
		
		for i in self.colls:
			
			value_check = 10*[False]
			
			for cell in i.cont:
				
				if cell.value ==0:
					return False
				
				elif value_check[cell.value]:
					return False
				
				else:
					value_check[cell.value] = True
		
		for i in self.rows:
			
			value_check = 10*[False]
			
			for cell in i.cont:
				
				if cell.value ==0:
					return False
				
				elif value_check[cell.value]:
					return False
				
				else:
					value_check[cell.value] = True
		
		for i in self.boxes:
			
			value_check = 10*[False]
			
			for cell in i.cont:
				
				if cell.value ==0:
					return False
				
				elif value_check[cell.value]:
					return False
				
				else:
					value_check[cell.value] = True		
		
		return True

	def backtrack(self,solution_count=0): 
		
		if solution_count>2:
			return solution_count
		
		global done; done = False
		
		for y in range(9):
			for x in range(9):
				
				if self.grid[y][x].value == 0:
					for i in range(1,10):
						
						if self.grid[y][x].cand[i] and self.possible(self.grid[y][x],i):
							
							self.val(x,y,i)
							output = self.backtrack(solution_count)
							
							if isinstance(output,int):
								solution_count = output
							
							else:
								solution_count=1
							
							if done ==True:
								done = False
								solution_count+=1
								global solution
								solution = deepcopy(self)
							
							self.val(x,y,0)
					
					if solution_count ==1:
						return solution
					return solution_count
		
		done =True
		
		if solution_count ==1:
			return solution
		return solution_count 
	
	def nakedsingle(self): #if cell has only one candidate, make it its value
		
		for y in range(9):
			for x in range(9):
				
				if self.grid[y][x].value == 0:
					if self.grid[y][x].cand_count() == 1:
						
						for i in range(1,10):
							
							if self.grid[y][x].cand[i]:
								self.val(x,y,i)
								return 1
					
					elif self.grid[y][x].cand_count() == 0:
						return -1
		
		return 0
	
	def hiddensingle(self): #if value is possilble only in one place in a house, make it its value 
		
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
					return 1
		
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
					return 1
		
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
					return 1
		
		return 0


							
						
						

