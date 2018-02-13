import numpy as np
import time

a = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
world_array = np.array(a)
world_adder = a[:]

def world(a, world_array, world_adder):
    for i in range(len(a)):
        coin_flip = np.random.randint(0, 2)
        if coin_flip == 0 and world_adder[0] != 1:
            world_adder.pop(0)
            world_adder.append(0)
        elif coin_flip == 1 and world_adder[-1] != 1:
            world_adder.pop(-1)
            world_adder.insert(0, 0)
        world_array = np.vstack((world_array, world_adder))
    
    return world_array

output = world(a, world_array, world_adder)

def move_right(output):
    world_adder = output[0]
    coin_flip = np.random.randint(0, 2)
    output = np.delete(output, -1, 0)
    if coin_flip == 0 and world_adder[0] != 1:
        world_adder = np.delete(world_adder, 0, 0)
        world_adder = np.append(world_adder, 0)
    if coin_flip == 1 and world_adder[-1] != 1:
        world_adder = np.delete(world_adder, -1, 0)
        world_adder = np.insert(world_adder, 0, 0, 0)
    output = np.vstack((world_adder, output))
    
#    print(world_adder[0])
    return output

for i in range(500):
    mr_output = move_right(output)
    output = mr_output[:]
    print(output)
    print("\n")
    time.sleep(.1)
#    if 1 in output[:, -1]:
#        break