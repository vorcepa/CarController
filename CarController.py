import numpy as np
import pygame as pg

'initializations'
pg.init()
display_width = 800
display_height = 600
gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Controller Car')

clock = pg.time.Clock()
world_seed = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
world_array = np.array(world_seed)

'''
Drawing the car and its location.
pg.draw.rect draws a simple rectangle.
arguments: surface (the game window), color (RGB tuple), coordinates and size (tuple)
'''
x = display_width * .45
y = display_height * .8
def car(x, y):
    pg.draw.rect(gameDisplay, (255, 255, 255), (x, y, 50, 50), 0)

'''
Array for the world.  Input is the world array,
which should be changing every frame(?).  World adder
copies some aspect of the world_array (currently the first
element, or in the game world the right-most drawn part of the world).
coin_flip determines if the next drawn road element (array index element == 1)
is one up or one down.

Returns world_array (first variable to use it is 'movement')
'''        
def world(world_array):
    if np.ndim(world_array) == 1:
        world_adder = np.copy(world_array)
    elif np.ndim(world_array) == 2:
        world_adder = world_array[0]
    else:
        print('world_array is neither 1 or 2 dimensions.  Something is wrong.')
        pg.quit()
    
    for i in range(len(world_adder)):
        coin_flip = np.random.randint(0, 2)
        if coin_flip == 0 and world_adder[0] != 1:
            world_adder = np.delete(world_adder, 0)
            world_adder = np.append(world_adder, 0)
        elif coin_flip == 1 and world_adder[-1] != 1:
            world_adder = np.delete(world_adder, -1)
            world_adder = np.insert(world_adder, 0, 0)
        world_array = np.vstack((world_array, world_adder))
    return world_array

def world_draw(world_array):
    rect_loc_x = int(display_width / len(world_array[0]))
    rect_loc_y = int(display_height / len(world_array[0]))
    
    for element in range(len(world_array)):
        for index in range(len(world_array[element])):
            if world_array[element][index] == 0:
                pg.draw.rect(gameDisplay, (255, 210, 0), (element*rect_loc_x, index*rect_loc_y, rect_loc_x, rect_loc_y))
            elif world_array[element][index] == 1:
                pg.draw.rect(gameDisplay, (128, 128, 128), (element*rect_loc_x, index*rect_loc_y, rect_loc_x, rect_loc_y))

m_right = world(world_array) #START POINT
world_draw(m_right)

def move_right(world_array):
    world_adder = world_array[-1]
    
    world_array = np.delete(world_array, 0, 0)
    coin_flip = np.random.randint(0, 2)
    if coin_flip == 0 and world_adder[0] != 1:
        world_adder = np.delete(world_adder, 0, 0)
        world_adder = np.append(world_adder, 0)
    if coin_flip == 1 and world_adder[-1] != 1:
        world_adder = np.delete(world_adder, -1, 0)
        world_adder = np.insert(world_adder, 0, 0, 0)
    world_array = np.vstack((world_array, world_adder))
    return world_array
    
    

#GAME LOGIC
temp_crashed = False

while not temp_crashed:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            temp_crashed = True
    
    m_right = move_right(m_right)
    world_draw(m_right)
    car(x, y)
    pg.display.update()
    clock.tick(10)
    
pg.quit()

