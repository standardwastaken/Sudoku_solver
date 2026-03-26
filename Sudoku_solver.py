from pygame import *
from sudoku import Sudoku
from random import randint
from copy import deepcopy
from webbrowser import open as wb_open 

#TODO hodne 
# docs
# support

#TODO idealne
# vic metod 


#window
screensize = (800,500)
caption ='Sudoku solver'

#colours
background = (200,200,200)
white = (185,185,220)
black = (0,0,0)
blue = (0,0,255)

#support
support_button_size = 30
support_link = 'https://github.com/standardwastaken/Sudoku_solver/blob/main/README.md'

# grid
messagefield_hight = 40
grid_outline= 5 
box_border = 2 #width of border between boxes
cell_size = 40
cell_outline = 1
grid_size = grid_outline*2+cell_size*9 + box_border*2

#menu
controls_hight = 35
function_hight = 45
controls_width = 80
menu_width = 3*controls_width
menu_grid_gab=100
menu_outline = 1

#fonts
message_font_size = 26
controls_font_size = (controls_width*2)//9
function_font_size = (function_hight*3)//5

#lu coordinates
grid_lug = support_button_size # grid left upper g coordinate
grid_luf = 5 # grid left upper f coordinate
controls_lug = grid_lug+grid_size+menu_grid_gab #controls left upper g coordinate 
controls_luf = grid_luf+grid_outline #controls left upper f coordinate
function_lug = grid_lug+grid_size+menu_grid_gab #function left upper g coordinate
function_luf = controls_luf+controls_hight+2*menu_outline #function left upper f coordinate

#messages
MSG_WELCOME = 'Welcome to Sudoku solver!'
MSG_NO_SOLUTION = 'This grid has no solution :('
MSG_MULTIPLE_SOLUTIONS = 'This grid has multiple solutions'
MSG_2_SOLUTIONS = 'This grid has 2 solutions'
MSG_NOT_SOLVABLE = 'Not solvable with chosen methods'
MSG_NO_HINT_FOUND = 'No hint found with chosen methods'
MSG_INVALID_MOVE = 'Invalid move!'

starting_grid = [['8', '0', '7', '0', '0', '0', '0', '0', '0'], 
					['0', '3', '1', '0', '0', '2', '4', '0', '0'],
					['0', '4', '0', '0', '0', '0', '0', '5', '2'],
					['9', '6', '0', '4', '1', '0', '8', '7', '0'],
					['1', '0', '0', '7', '0', '3', '9', '2', '0'],
					['0', '0', '4', '9', '0', '8', '1', '0', '0'],
					['4', '0', '6', '1', '0', '7', '2', '3', '0'],
					['7', '5', '3', '0', '0', '0', '0', '9', '1'],
					['0', '1', '0', '0', '0', '6', '5', '0', '0']]

controls = [' Solve (S)',' Hint (H)',' Clear (C)']

NAKEDSINGLE = 'Naked single'
HIDDENSINGLE = 'Hidden single'
BACKTRACKING = 'Backtracking'

functions={NAKEDSINGLE:True,HIDDENSINGLE:True,BACKTRACKING:True} 
functions_keys = [*functions.keys()]


selected_cell = [False,0,0] 
solution = None



def screen_draw(message=''): 
	
	#background
	window.fill(background)
	
	#grid background
	draw.rect(window,(0,0,0),(grid_lug,grid_luf+messagefield_hight,grid_size,grid_size))
	
	#message
	if message !='':
		text = font.SysFont("Segoe UI Symbol",message_font_size).render(' '+message,1,black)
		window.blit(text,(grid_lug, grid_luf, grid_size, messagefield_hight))

	#draw cells
	for y in range(9):
		for x in range(9):
			
			draw.rect(window, (230,230,255),(grid_lug+grid_outline+cell_size*x + box_border*(x//3),
										grid_luf+messagefield_hight+grid_outline+cell_size*y + box_border*(y//3),
										cell_size,cell_size))
			
			draw.rect(window, (0,0,0),(grid_lug+grid_outline+cell_size*x + box_border*(x//3),
										grid_luf+messagefield_hight+grid_outline+cell_size*y + box_border*(y//3),
										cell_size,cell_size),cell_outline)
	
	#highhilight selected cell
	if selected_cell[0]:
		cell_highlight(selected_cell[1],selected_cell[2])
	
	#draw filled values
	for y in range(9):
		for x in range(9):
			if Board.grid[y][x].value != 0:
				text = font.SysFont("notosans",cell_size).render(str(Board.grid[y][x].value),1,(0,0,0))
				window.blit(text, (cell_size//2+grid_lug+grid_outline+cell_size*x + box_border*(x//3)-(2/7)*cell_size,
										grid_luf+messagefield_hight+grid_outline+cell_size*y + box_border*(y//3)-(1/5)*cell_size,
										cell_size,cell_size))
	
	#controls
	draw.rect(window,black,(controls_lug, controls_luf, menu_width+2*menu_outline,controls_hight+2*menu_outline))
	
	for i in range(3):
		
		draw.rect(window,white, (controls_lug+menu_outline+i*controls_width,controls_luf+menu_outline,controls_width,controls_hight),)
		
		draw.rect(window,black, (controls_lug+menu_outline+i*controls_width,controls_luf+menu_outline,controls_width,controls_hight),menu_outline)
		
		text = font.SysFont("Segoe UI Symbol",controls_font_size).render(controls[i],1,black)
		window.blit(text, (controls_lug+menu_outline+i*controls_width,controls_luf+menu_outline+controls_hight//6,controls_width,controls_hight))

	#function menu
	draw.rect(window,black, (function_lug,function_luf, menu_width+2*menu_outline,len(functions_keys)*function_hight+2*menu_outline))
	
	for i in range(len(functions_keys)):
		
		draw.rect(window, white, (function_lug+menu_outline,function_luf+menu_outline+function_hight*i, menu_width, function_hight))
		
		draw.rect(window, black, (function_lug+menu_outline,function_luf+menu_outline+function_hight*i, menu_width, function_hight),menu_outline)
		
		text = font.SysFont("Segoe UI Symbol",function_font_size).render(func_icon(i)+str(functions_keys[i]),1,(20,120,20) if functions[functions_keys[i]] else (100,0,0))
		window.blit(text,(function_lug+menu_outline,function_luf+menu_outline+function_hight*i, menu_width, function_hight))
	
	#support
	draw.rect(window,blue,(0,0,support_button_size,support_button_size))
	text = font.SysFont("notosans",(support_button_size*3)//4).render('?',1,white)
	window.blit(text,(support_button_size//3,0,support_button_size,support_button_size))


	display.update()


def func_icon(i):
	
	if functions[functions_keys[i]]:
		return ' ☑ '
	else:
		return ' ☒ '

def func_select(i):
	
	functions[functions_keys[i]] = not functions[functions_keys[i]]
	screen_draw()

def controls_select(i): 
	
	if i==0:
		solve(Board)
	
	elif i==1:
		hint(Board)
	
	elif i==2:
		clear(Board)
	

def cell_select(Selected=False,x_change=0,y_change=0):
	
	global selected_cell; 
	
	x = selected_cell[1]+x_change
	y = selected_cell[2]+y_change

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
	
	screen_draw()

def cell_select_up(self=None):
	cell_select(True,0,-1)

def cell_select_down(self=None):
	cell_select(True,0,1)

def cell_select_left(self=None):
	cell_select(True,-1,0)

def cell_select_right(self=None):
	cell_select(True,1,0)


def cell_highlight(x,y):
	
	draw.rect(window, (230,230,0),(grid_lug+grid_outline+cell_size*x + box_border*(x//3),
                                	grid_luf+messagefield_hight+grid_outline+cell_size*y + box_border*(y//3),
                                	cell_size,cell_size))
	
	draw.rect(window, (0,0,0),(grid_lug+grid_outline+cell_size*x + box_border*(x//3),
                                	grid_luf+messagefield_hight+grid_outline+cell_size*y + box_border*(y//3),
                                	cell_size,cell_size),cell_outline)


def insert(self,value): #insert value in cell and move selected cell
	
	global selected_cell
	x = selected_cell[1]
	y= selected_cell[2]
	
	try:
		self.val(x,y,value)
		
		if value > 0 or self.grid[selected_cell[2]][selected_cell[1]].value ==0:
			cell_select(True,selected_cell[1]+1,selected_cell[2])
		
		screen_draw()
	
	except:
		screen_draw(MSG_INVALID_MOVE)	

def insert_1(self):
	insert(self,1)

def insert_2(self):
	insert(self,2)

def insert_3(self):
	insert(self,3)

def insert_4(self):
	insert(self,4)

def insert_5(self):
	insert(self,5)

def insert_6(self):
	insert(self,6)

def insert_7(self):
	insert(self,7)

def insert_8(self):
	insert(self,8)

def insert_9(self):
	insert(self,9)

def insert_0(self):
	insert(self,0)


def solve(self):
	
	if self.solved():
		return
	
	while True:
		unsolved = True 
		
		if functions[NAKEDSINGLE]:
			
			if self.nakedsingle() ==1:
				unsolved = False
				screen_draw()
			
			elif self.nakedsingle() ==-1:	
				screen_draw(MSG_NO_SOLUTION)
		
		elif functions[HIDDENSINGLE]:
			
			if self.hiddensingle() ==1:
				unsolved = False
				screen_draw()
		
		if unsolved:
			break
	
	if self.solved():
		return
	
	if functions[BACKTRACKING]:
		
		solution = self.backtrack()
		
		if isinstance(solution,Sudoku):
			
			self.grid = deepcopy(solution.grid)
			screen_draw()
		
		elif solution == 0:
			screen_draw(MSG_NO_SOLUTION)
		
		elif solution ==2:
			screen_draw(MSG_2_SOLUTIONS)
		
		elif solution >2:
			screen_draw(MSG_MULTIPLE_SOLUTIONS)
	
	else:
		screen_draw(MSG_NOT_SOLVABLE)
		
def hint(self):
	
	if Board.solved() >0:
		return
	
	if functions[NAKEDSINGLE]:
		
		if self.nakedsingle():
			screen_draw()
			return
	
	if functions[HIDDENSINGLE]:
		
		if self.hiddensingle():
			screen_draw()
			return
	
	if functions[BACKTRACKING]:
		
		global solution
		
		if solution == None:
			solution = self.backtrack()
		
		if isinstance(solution,Sudoku):
			
			x = randint(0,8)
			y = randint(0,8)
			
			while self.grid[y][x].value !=0:
				x = randint(0,8)
				y = randint(0,8)
			
			self.val(x,y,solution.grid[y][x].value)
			screen_draw()
		
		elif solution == 0:
			screen_draw(MSG_NO_SOLUTION)
		
		elif solution ==2:
			screen_draw(MSG_2_SOLUTIONS)
		
		elif solution >2:
			screen_draw(MSG_MULTIPLE_SOLUTIONS)	
		
		return
	
	else:
		screen_draw(MSG_MULTIPLE_SOLUTIONS)

def clear(self):
	
	self.__init__()
	screen_draw()

def support(self=None):
	
	wb_open(support_link)


def mouse_select():
	
	g,f = mouse.get_pos()
	
	if (g > grid_lug+grid_outline and g < grid_lug+grid_size-grid_outline) and (f > grid_luf+messagefield_hight+grid_outline and f < grid_luf+messagefield_hight+grid_size-grid_outline):
		
		box_size = cell_size*3+box_border
		
		g=g-(grid_lug+grid_outline)
		boxx= g//box_size
		g = g - boxx*box_size
		x = g//cell_size+3*boxx

		f=f-(grid_luf+messagefield_hight+grid_outline)
		boxy= f//box_size
		f = f - boxy*box_size
		y = f//cell_size+3*boxy
		
		cell_select(True,x,y)
	
	elif (g>function_lug+menu_outline and g<function_lug+menu_outline+menu_width) and (f>function_luf+menu_outline and f<function_luf+menu_outline+function_hight*len(functions_keys)):
		
		f=f-(function_luf+menu_outline)
		i = f//function_hight
		
		func_select(i)
	
	elif (g>controls_lug+menu_outline and g<controls_lug+menu_width+menu_outline) and (f>controls_luf+menu_outline and f<controls_luf+controls_hight+menu_outline):
		
		g=g-(controls_lug+menu_outline)
		i = g//controls_width
		
		controls_select(i)
	
	elif g<support_button_size and f<support_button_size:
		support()
	else:
		cell_select()


keys = {K_s:	solve,
		K_h:	hint,
		K_c:	clear,
		
		K_F1:	support,
		
		K_LEFT:		cell_select_left,
		
		K_RIGHT:	cell_select_right,
		K_TAB:		cell_select_right,
		
		K_UP:		cell_select_up,
		
		K_DOWN:		cell_select_down,
		K_KP_ENTER:	cell_select_down,
		K_RETURN:	cell_select_down,
		
		K_1:	insert_1,
		K_KP_1:	insert_1,
		K_2:	insert_2,
		K_KP_2:	insert_2,
		K_3:	insert_3,
		K_KP_3:	insert_3,
		K_4:	insert_4,
		K_KP_4:	insert_4,
		K_5:	insert_5,
		K_KP_5:	insert_5,
		K_6:	insert_6,
		K_KP_6:	insert_6,
		K_7:	insert_7,
		K_KP_7:	insert_7,
		K_8:	insert_8,
		K_KP_8:	insert_8,
		K_9:	insert_9,
		K_KP_9:	insert_9,
		
		K_0:			insert_0,
		K_KP_0:			insert_0,
		K_BACKSPACE:	insert_0,
		K_SPACE:		insert_0,}


init()
display.init()

window = display.set_mode(screensize, RESIZABLE)
display.set_caption(caption)

Board = Sudoku()
Board.import_list(starting_grid)

screen_draw(MSG_WELCOME)

running = True

while running:	 
	
	for i in event.get():
		
		if i.type == QUIT:
			running = False
		
		if i.type == MOUSEBUTTONDOWN:
			mouse_select()
		
		if i.type == KEYDOWN:
			
			try:
				
				keys[i.key](Board)
			
			except:
				pass
			
			
			
