import math, random, sys
import pygame as pg
import WorldArray

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
FPS = 500

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GOLD = (255, 210, 0)
GREY = (128, 128, 128)

# background
class WorldBlock():
    def __init__(self, xpos, ypos):
        self.image = pg.Surface((int(W/10), int(H/10)))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        
worldblocks = [[] for _ in range(len(WorldArray.world))]
for element in range(len(WorldArray.world)):
    for index in range(len(WorldArray.world[element])):
        worldblocks[element].append(WorldBlock(int(W/10)*element, int(H/10)*index))
        if WorldArray.world[element][index] == 0:
            worldblocks[element][index].image.fill((GOLD))
        else:
            worldblocks[element][index].image.fill((GREY))

#player info
startScrollingPosX = HW
circleRadius = 25
circlePosX = circleRadius

playerPosX = circleRadius
playerPosY = circleRadius * 2#CHANGE LATER
playerVelocityX = 0
playerVelocityY = 0
stagePosX = 0

# main loop
while True:
    events()
    
    #movement
    k = pg.key.get_pressed()
    if k[pg.K_RIGHT]:
        playerVelocityX = 1
        playerVelocityY = 0
    elif k[pg.K_LEFT]:
        playerVelocityX = -1
        playerVelocityY = 0
    elif k[pg.K_UP]:
        playerVelocityY = -1
        playerVelocityX = 0
    elif k[pg.K_DOWN]:
        playerVelocityY = 1
        playerVelocityX = 0
    else:
        playerVelocityX = 0
        playerVelocityY = 0
    
    playerPosX += playerVelocityX
    playerPosY += playerVelocityY

    for i in range(len(worldblocks)):
        for j in range(len(worldblocks[i])):
            DS.blit(worldblocks[i][j].image, worldblocks[i][j].rect)    
            
    pg.draw.circle(DS, WHITE, (int(playerPosX), int(playerPosY) - circleRadius), circleRadius, 0)
            
    pg.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)