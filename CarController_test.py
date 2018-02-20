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
bg = WorldArray.world
def WorldDraw(bg):
    pos_x = int(W / 10)
    pos_y = int(H / 10)
    size_x = pos_x*1.15
    size_y = pos_y*1.15
    
    for element in range(len(bg)):
        for index in range(len(bg[element])):
            if bg[element][index] == 0:
                pg.draw.rect(DS, (GOLD), (pos_x*element, pos_y*index, size_x, size_y))
            elif bg[element][index] == 1:
                pg.draw.rect(DS, (GREY), (pos_x*element, pos_y*index, size_x, size_y))
    
    stageWidth = size_x * len(bg[0])
    stageHeight = size_y * len(bg[0])
    
    return (stageWidth, stageHeight)

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
    stageWidth, stageHeight = WorldDraw(bg)
    
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
    
    if playerPosX > stageWidth - circleRadius:
        playerPosX = stageWidth - circleRadius
    if playerPosX < circleRadius:
        playerPosX = circleRadius
    if playerPosX < startScrollingPosX:
        circlePosX = playerPosX
    elif playerPosX > stageWidth - startScrollingPosX:
        circlePosX = playerPosX - stageWidth + W
    else:
        circlePosX = startScrollingPosX
        stagePosX += -playerVelocityX
    
    
    pg.draw.circle(DS, WHITE, (int(circlePosX), int(playerPosY) - circleRadius), circleRadius, 0)
        
    pg.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)