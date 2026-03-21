#TODO hodne 
# solved()
# gui  No / Multiple solutions 
# docs
#TODO stredne
# hezci barvy?
# uklidit: vsechny todo, tweakables, fce (i v Sudoku) zkonsistentnit x,z ; g,f
# uklidit coordinates of grid and cells
#TODO idealne
# vic metod, 16 a 25 gridy 

from pygame import *
from sudoku import Sudoku
from random import randint
from copy import deepcopy
init()
display.init()

screensize = (800,500)#(1600,1000) #TODO  jina screensize?
window = display.set_mode(screensize)
window.fill((200,200,200))
selected_cell = [False,0,0] #TODO reference na konkretni cell?
solution = None

white = (185,185,220)
black = (0,0,0)


#tweakables #TODO rename
border_offset = 40 
outline_offset= 5
small_offset = 0
big_offset = 2
cell_size = 40
cell_outline = 1
outline_size = outline_offset*2+cell_size*9 + big_offset*2

#menu
controls_hight = 35
function_hight = 45
controls_width = 80
menu_width = 3*controls_width
menu_grid_gab=100
menu_outline = 1

controls_font_size = (controls_width*2)//9
function_font_size = (function_hight*3)//5

controls = [' Solve (S)',' Hint (H)',' Clear (C)']
functions={'Naked single':False,'Hidden single':False,'Backtracking':False} #TODO change all to true
functions_keys = [*functions.keys()]

controls_lux = border_offset+outline_size+menu_grid_gab #controls left upper x coordinate #TODO rename
controls_luy = border_offset+outline_offset #controls left upper y coordinate
function_lux = border_offset+outline_size+menu_grid_gab #function left upper x coordinate
function_luy = controls_luy+controls_hight+2*menu_outline #function left upper y coordinate









def grid_draw(): #rename
	#background
	window.fill((200,200,200))
	#grid background
	draw.rect(window,(0,0,0),(border_offset,border_offset,outline_size,outline_size))
	#draw.rect(window,(50,0,250),(20,20,outline_size,outline_size),2)
	#draw cells
	for y in range(9):
		for x in range(9):
			draw.rect(window, (230,230,255),(border_offset+outline_offset+cell_size*x + big_offset*(x//3),
										border_offset+outline_offset+cell_size*y + big_offset*(y//3),
										cell_size,cell_size))
			draw.rect(window, (0,0,0),(border_offset+outline_offset+cell_size*x + big_offset*(x//3),
										border_offset+outline_offset+cell_size*y + big_offset*(y//3),
										cell_size,cell_size),cell_outline)
	#highhilight selected cell
	if selected_cell[0]:
		cell_highlight(selected_cell[1],selected_cell[2])
	#draw filled values
	for y in range(9):
		for x in range(9):
			if Board.grid[y][x].value != 0:
				text = font.SysFont("notosans",cell_size).render(str(Board.grid[y][x].value),1,(0,0,0))
				window.blit(text, (cell_size/2+border_offset+outline_offset+cell_size*x + big_offset*(x//3)-(2/7)*cell_size,
										border_offset+outline_offset+cell_size*y + big_offset*(y//3)-(1/5)*cell_size,
										cell_size,cell_size))
	
	#controls

	draw.rect(window,black,(controls_lux, controls_luy, menu_width+2*menu_outline,controls_hight+2*menu_outline))
	for i in range(3):
		draw.rect(window,white, (controls_lux+menu_outline+i*controls_width,controls_luy+menu_outline,controls_width,controls_hight),)
		draw.rect(window,black, (controls_lux+menu_outline+i*controls_width,controls_luy+menu_outline,controls_width,controls_hight),menu_outline)
		text = font.SysFont("Segoe UI Symbol",controls_font_size).render(controls[i],1,black)
		window.blit(text, (controls_lux+menu_outline+i*controls_width,controls_luy+menu_outline+controls_hight//6,controls_width,controls_hight))

	#function menu

	draw.rect(window,black, (function_lux,function_luy, menu_width+2*menu_outline,len(functions_keys)*function_hight+2*menu_outline))
	for i in range(len(functions_keys)):
		draw.rect(window, white, (function_lux+menu_outline,function_luy+menu_outline+function_hight*i, menu_width, function_hight))
		draw.rect(window, black, (function_lux+menu_outline,function_luy+menu_outline+function_hight*i, menu_width, function_hight),menu_outline)
		text = font.SysFont("Segoe UI Symbol",function_font_size).render(func_icon(i)+str(functions_keys[i]),1,(20,120,20) if functions[functions_keys[i]] else (100,0,0))
		window.blit(text,(function_lux+menu_outline,function_luy+menu_outline+function_hight*i, menu_width, function_hight))
	
	display.update()

def controls_select(i): #TODO zrusit
	if i==0:
		solve(Board)
	elif i==1:
		hint(Board)
	elif i==2:
		clear(Board)

def func_select(i): #TODO zrusit
	functions[functions_keys[i]] = not functions[functions_keys[i]]
	grid_draw()

def func_icon(i):
	if functions[functions_keys[i]]:
		return ' ☑ '
	else:
		return ' ☒ '
	
def cell_select(Selected=False,x=0,y=0):
	global selected_cell
	if (x>8 and y==8) or (x==8 and y>8):
		x=0
		y=0
	if (x<0 and y==0) or (x==0 and y<0):
		x=8
		y=8
	if x>8:
		x=0
		y+=1
	elif x<0:
		x=8
		y-=1
	if y>8:
		x+=1
		y=0
	elif y<0:
		x-=1
		y=8	
	selected_cell = [Selected,x,y]
	grid_draw()

def cell_highlight(x,y):
	draw.rect(window, (230,230,0),(border_offset+outline_offset+cell_size*x + big_offset*(x//3),
                                	border_offset+outline_offset+cell_size*y + big_offset*(y//3),
                                	cell_size,cell_size))
	draw.rect(window, (0,0,0),(border_offset+outline_offset+cell_size*x + big_offset*(x//3),
                                	border_offset+outline_offset+cell_size*y + big_offset*(y//3),
                                	cell_size,cell_size),cell_outline)

def mouse_select():
	g,f = mouse.get_pos()
	if (g > border_offset+outline_offset and g < border_offset+outline_size-outline_offset) and (f > border_offset+outline_offset and f < border_offset+outline_size-outline_offset):
		box_size = cell_size*3+big_offset
		g=g-border_offset-outline_offset
		boxx= g//box_size
		g = g - boxx*box_size
		x = g//cell_size+3*boxx

		f=f-border_offset-outline_offset
		boxy= f//box_size
		f = f - boxy*box_size
		y = f//cell_size+3*boxy
		cell_select(True,x,y)
	elif (g>function_lux+menu_outline and g<function_lux+menu_outline+menu_width) and (f>function_luy+menu_outline and f<function_luy+menu_outline+function_hight*len(functions_keys)):
		f=f-function_luy-menu_outline
		i = f//function_hight
		func_select(i)
	elif (g>controls_lux+menu_outline and g<controls_lux+menu_width+menu_outline) and (f>controls_luy+menu_outline and f<controls_luy+controls_hight+menu_outline):
		g=g-controls_lux-menu_outline
		i = g//controls_width
		controls_select(i)
	else:
		cell_select()

def insert(self,value): #insert value in cell and move selected cell
	global selected_cell
	x = selected_cell[1]
	y= selected_cell[2]
	if value > 0 or self.grid[selected_cell[2]][selected_cell[1]].value ==0:
		cell_select(True,selected_cell[1]+1,selected_cell[2])
	self.val(x,y,value)
	grid_draw()

def solve(self):#solvne cely sudoku, postupne v loopu vola dílčí fce
	if self.solved():
		return
	while True:
		unsolved = True
		if functions['Naked single']:
			if self.nakedsingle():
				unsolved = False
				grid_draw()
		elif functions['Hidden single']:
			if self.hiddensingle():
				unsolved = False
				grid_draw()
		if unsolved:
			break
	if functions['Backtracking']:
		solution = self.backtrack()
		if isinstance(solution,Sudoku):
			print(solution)
			self.grid = deepcopy(solution.grid)
		elif solution == 0:
			raise Exception('No solutions')
		elif solution ==2:
			raise Exception('Multiple solutions')
		
	grid_draw()

def hint(self):
	if Board.solved() >0:
		return
	if functions['Naked single']:
		if self.nakedsingle():
			grid_draw()
			return
	elif functions['Hidden single']:
		if self.hiddensingle():
			grid_draw()
			return
	elif functions['Backtracking']:
		global solution
		if solution == None:
			solution = self.backtrack()
		if isinstance(solution,Sudoku):
			x = randint
			y = randint
			while self.grid[y][x].value !=0:
				x = randint
				y = randint
			self.grid[y][x] == deepcopy(solution.grid[y][x])
			grid_draw()
		elif solution == 0:
			raise Exception('No solutions')
		elif solution >1:
			raise Exception('Multiple solutions')


		return

def clear(self):
	self.__init__()
	grid_draw()



Board = Sudoku()
Board.vloz_zadani([['8', '0', '7', '0', '0', '0', '0', '0', '0'],
					['0', '3', '1', '0', '0', '2', '4', '0', '0'],
					['0', '4', '0', '0', '0', '0', '0', '5', '2'],
					['9', '6', '0', '4', '1', '0', '8', '7', '0'],
					['1', '0', '0', '7', '0', '3', '9', '2', '0'],
					['0', '0', '4', '9', '0', '8', '1', '0', '0'],
					['4', '0', '6', '1', '0', '7', '2', '3', '0'],
					['7', '5', '3', '0', '0', '0', '0', '9', '1'],
					['0', '1', '0', '0', '0', '6', '5', '0', '0']])
grid_draw()
running = True
while running:	
	for i in event.get():
		if i.type == QUIT:
			running = False
		if i.type == MOUSEBUTTONDOWN:
			mouse_select()
		if i.type == KEYDOWN:
			if i.key == K_d:
				print(Board.grid[selected_cell[2]][selected_cell[1]].cand)
			if i.key == K_s:
				solve(Board)
			if i.key == K_h:
				hint(Board)
			if i.key == K_c:
				clear(Board)
			if i.key == K_LEFT:
				cell_select(True,selected_cell[1]-1, selected_cell[2])
			if i.key == K_RIGHT or i.key == K_TAB:
				cell_select(True,selected_cell[1]+1, selected_cell[2])
			if i.key == K_UP:
				cell_select(True,selected_cell[1], selected_cell[2]-1)
			if i.key == K_DOWN or i.key == K_KP_ENTER or i.key == K_RETURN:
				cell_select(True,selected_cell[1], selected_cell[2]+1)
			if i.key == K_1 or i.key == K_KP_1:
				insert(Board,1)
			if i.key == K_2 or i.key == K_KP_2:
				insert(Board,2)
			if i.key == K_3 or i.key == K_KP_3:
				insert(Board,3)
			if i.key == K_4 or i.key == K_KP_4:
				insert(Board,4)
			if i.key == K_5 or i.key == K_KP_5:
				insert(Board,5)
			if i.key == K_6 or i.key == K_KP_6:
				insert(Board,6)
			if i.key == K_7 or i.key == K_KP_7:
				insert(Board,7)
			if i.key == K_8 or i.key == K_KP_8:
				insert(Board,8)
			if i.key == K_9 or i.key == K_KP_9:
				insert(Board,9)
			if i.key == K_0 or i.key == K_KP_0 or i.key == K_BACKSPACE or i.key == K_SPACE:
				insert(Board,0)