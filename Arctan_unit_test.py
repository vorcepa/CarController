import math
import time
import numpy as np
s = time.time()

def __get_slope(sensorInfo, rOffsets, radian):
    arctans = []
    coords = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    for i in coords:
        arctans.append(np.arctan2(i[1], i[0]))
        if arctans[-1] < 0:
            arctans[-1] = 2*math.pi + arctans[-1]

    return arctans


if __name__ == "__main__":
    output = __get_slope(1, 2, 3)
    f = time.time()
    print(output, s-f)
