import WorldArray
import pygame as pg
import sys, time

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
FPS = 60 

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
worldblocks = worldDraw(worldblocks_blank, world_test)

gameActive = True

while gameActive:
    events()
    
    k = pg.key.get_pressed()
    if k[pg.K_RIGHT]:
        for lists in worldblocks:
            for block in lists:
                block.rect.x += -2
    elif k[pg.K_LEFT]:
        for lists in worldblocks:
            for block in lists:
                block.rect.x += 2
    elif k[pg.K_UP]:
        for lists in worldblocks:
            for block in lists:
                block.rect.y += 2
    elif k[pg.K_DOWN]:
        for lists in worldblocks:
            for block in lists:
                block.rect.y += -2
    
    DS.fill((0,0,0))    
    for i in range(len(worldblocks)):
        for j in range(len(worldblocks[i])):
            DS.blit(worldblocks[i][j].image, worldblocks[i][j].rect)
    
    pg.display.update()
    CLOCK.tick(FPS)