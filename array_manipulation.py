import numpy as np

world_seed = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
world_array = np.array(world_seed)

test_array = np.vstack((world_seed, world_array))

#world_adder = test_array[0]

print(np.ndim(test_array))