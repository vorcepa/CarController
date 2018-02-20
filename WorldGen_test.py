import WorldArray
import pygame as pg
import sys

worldArray = WorldArray.world
#print(worldArray)

# exit the program
def events():
	for event in pg.event.get():
		if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
			pg.quit()
			sys.exit()

# define display surface			
W, H = 800, 600
HW, HH = W / 2, H / 2
AREA = W * H
# initialise display
pg.init()
CLOCK = pg.time.Clock()
DS = pg.display.set_mode((W, H))
pg.display.set_caption("code.Pylet - Scrolling Background with Player")
FPS = .25

class WorldBlock():
    def __init__(self, xpos, ypos):
        self.image = pg.Surface((int(W/10), int(H/10)))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        
worldblocks_blank = [[] for _ in range(len(WorldArray.world))]
world_test = WorldArray.world

def worldDraw(worldblocks_blank, world_test):
    worldblocks = worldblocks_blank[:]
    world = world_test
    
    for a in range(len(world)):
        for b in range(len(world[a])):
            worldblocks[a].append(WorldBlock(int(W/10)*a, int(H/10)*b))
            if world[a][b] == 0:
                worldblocks[a][b].image.fill((255, 210, 0))
            else:
                worldblocks[a][b].image.fill((128, 128, 128))
    
    return worldblocks

#worldblocks = worldblocks_blank[:]
#for element in range(len(WorldArray.world)):
#    for index in range(len(WorldArray.world[element])):
#        worldblocks[element].append(WorldBlock(int(W/10)*element, int(H/10)*index))
#        if WorldArray.world[element][index] == 0:
#            worldblocks[element][index].image.fill((255, 210, 0))
#        else:
#            worldblocks[element][index].image.fill((128, 128, 128))
                
gameActive = True

while gameActive:
    events()
    
    worldblocks = worldDraw(worldblocks_blank, world_test)
    
    for i in range(len(worldblocks)):
        for j in range(len(worldblocks[i])):
            DS.blit(worldblocks[i][j].image, worldblocks[i][j].rect)
    
    pg.display.update()