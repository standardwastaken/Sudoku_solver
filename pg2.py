#https://openclipart.org/detail/191039/yes-mark

from pygame import *
from sudoku import Sudoku
init()
display.init()


screensize = (1000,500)
window = display.set_mode(screensize)
window.fill((200,200,200))



#tweakables
border_offset = 20
outline_offset= 5
small_offset = 2
big_offset = 2
cell_size = 40
grid_func_gab=100
function_outline =5
function_offset = 3
function_hight = 40
function_width = 250

box_size = ((cell_size+small_offset)*3)+big_offset
outline_size = outline_offset*2+(cell_size+small_offset)*9 + big_offset*2
selected_cell = [False,0,0]

#functions
functions={'Naked single':True,'Hidden single':True,'Backtracking':True}
functions_keys = [*functions.keys()]



def grid_draw():
	#background
	window.fill((200,200,200))
	#grid background
	draw.rect(window,(0,0,0),(border_offset,border_offset,outline_size,outline_size))
	draw.rect(window,(50,0,250),(20,20,outline_size,outline_size),2)
	#draw cells
	for y in range(9):
		for x in range(9):
			draw.rect(window, (230,230,255),(border_offset+outline_offset+(cell_size+small_offset)*x + big_offset*(x//3),
										border_offset+outline_offset+(cell_size+small_offset)*y + big_offset*(y//3),
										cell_size,cell_size))
	#highhilight selected cell
	if selected_cell[0]:
		cell_highlight(selected_cell[1],selected_cell[2])
	#draw filled values
	for y in range(9):
		for x in range(9):
			if Board.grid[y][x].value != 0:
				value = font.SysFont("notosans",cell_size).render(str(Board.grid[y][x].value),1,(0,0,0))
				window.blit(value, (cell_size/2+border_offset+outline_offset+(cell_size+small_offset)*x + big_offset*(x//3)-(2/7)*cell_size,
										border_offset+outline_offset+(cell_size+small_offset)*y + big_offset*(y//3)-(1/5)*cell_size,
										cell_size,cell_size))
	#function menu
	draw.rect(window,(150,150,255), (border_offset+outline_size+grid_func_gab, border_offset, function_width+2*function_outline, len(functions_keys)*(function_hight+function_offset)-function_offset+2*function_outline))
	for i in range(len(functions_keys)):
		draw.rect(window, (20,20,255), (border_offset +outline_size+grid_func_gab+function_outline, border_offset+(function_hight+function_offset)*i+function_outline, function_width, function_hight))
		value = font.SysFont("Segoe UI Symbol",(function_hight//4)*3).render(func_icon(i)+str(functions_keys[i]),1,(0,255,0) if functions[functions_keys[i]] else (255,0,0))
		window.blit(value,(border_offset +outline_size+grid_func_gab+function_outline, border_offset+(function_hight+function_offset)*i+function_outline, function_width, function_hight))
	
	display.update()

def func_select(i):
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
	draw.rect(window, (230,230,0),(border_offset+outline_offset+(cell_size+small_offset)*x + big_offset*(x//3),
                                	border_offset+outline_offset+(cell_size+small_offset)*y + big_offset*(y//3),
                                	cell_size,cell_size))

def mouse_select():
	g,f = mouse.get_pos()
	if (g > border_offset+outline_offset and g < border_offset+outline_offset+outline_size) and (f > border_offset+outline_offset and f < border_offset+outline_offset+outline_size):
		g=g-border_offset-outline_offset
		boxx= g//box_size
		g = g - boxx*box_size
		x = g//(cell_size+small_offset)+3*boxx

		f=f-border_offset-outline_offset
		boxy= f//box_size
		f = f - boxy*box_size
		y = f//(cell_size+small_offset)+3*boxy
		cell_select(True,x,y)
	elif (g>border_offset+outline_size+grid_func_gab+function_outline and g<border_offset+outline_size+grid_func_gab+function_outline+function_width) and (f>border_offset+function_outline and f<border_offset+function_outline+(function_hight+function_offset)*len(functions_keys)):
		f=f-border_offset-function_outline
		i = f//(function_hight+function_offset)
		func_select(i)
	else:
		cell_select()

def insert(value):
	global selected_cell
	x = selected_cell[1]
	y= selected_cell[2]
	Board.grid[y][x].value=value
	cell_select(True,selected_cell[1]+1,selected_cell[2])
	grid_draw()

def solve(self,zadani=0):#solvne cely sudoku, postupne v loopu vola dílčí fce
		self.vloz_zadani(zadani)
		print("jdu na to")
		while True:
			if functions['Naked single']:
				if self.nakedsingle():
					grid_draw()
			elif functions['Hidden single']:
				if self.hiddensingle():
					grid_draw()
			else:
				break
		self.backtrack()
Board = Sudoku()
Board.vloz_zadani([['0', '0', '0', '0', '2', '0', '6', '0', '0'],
					['0', '0', '0', '0', '0', '0', '0', '7', '4'],
					['0', '0', '0', '9', '1', '0', '0', '0', '0'],
					['0', '2', '0', '0', '0', '0', '0', '0', '9'],
					['4', '1', '6', '0', '0', '0', '0', '0', '0'],
					['0', '9', '0', '4', '0', '0', '5', '0', '0'],
					['0', '0', '0', '0', '6', '0', '0', '5', '0'],
					['7', '0', '0', '1', '0', '2', '0', '0', '0'],
					['6', '0', '8', '0', '0', '0', '0', '3', '0']])
grid_draw()
running = True
while running:	
	for i in event.get():
		if i.type == QUIT:
			running = False
		if i.type == MOUSEBUTTONDOWN:
			mouse_select()
		if i.type == KEYDOWN:
			if i.key == K_s:
				Board.main()
				grid_draw()
			if i.key == K_LEFT:
				cell_select(True,selected_cell[1]-1, selected_cell[2])
			if i.key == K_RIGHT or i.key == K_TAB:
				cell_select(True,selected_cell[1]+1, selected_cell[2])
			if i.key == K_UP:
				cell_select(True,selected_cell[1], selected_cell[2]-1)
			if i.key == K_DOWN or i.key == K_KP_ENTER or i.key == K_RETURN:
				cell_select(True,selected_cell[1], selected_cell[2]+1)
			if i.key == K_1:
				insert(1)
			if i.key == K_KP_1:
				insert(1)
			if i.key == K_2:
				insert(2)
			if i.key == K_KP_2:
				insert(2)
			if i.key == K_3:
				insert(3)
			if i.key == K_KP_3:
				insert(3)
			if i.key == K_4:
				insert(4)
			if i.key == K_KP_4:
				insert(4)	
			if i.key == K_5:
				insert(5)
			if i.key == K_KP_5:
				insert(5)
			if i.key == K_6:
				insert(6)
			if i.key == K_KP_6:
				insert(6)	
			if i.key == K_7:
				insert(7)
			if i.key == K_KP_7:
				insert(7)	
			if i.key == K_8:
				insert(8)
			if i.key == K_KP_8:
				insert(8)
			if i.key == K_9:
				insert(9)
			if i.key == K_KP_9:
				insert(9)	
			if i.key == K_0:
				insert(0)
			if i.key == K_KP_0:
				insert(0)	
			if i.key == K_BACKSPACE:
				insert(0)
			if i.key == K_SPACE:
				insert(0)