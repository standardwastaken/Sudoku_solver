from pygame import *
init()
display.init()
screensize = (1800,1000)
window = display.set_mode(screensize)
window.fill((255,255,255))

#construct
x = [font.get_fonts()]
for i in range(len(x)):
    value = font.SysFont(x[i],30).render('☒☑',0,(0,0,0))
    window.blit(value, (30*(i%30),30*(i//30)))
display.update()


running = True
while running:
    for i in event.get():
        if i.type == QUIT:
            running = False