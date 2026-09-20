import numpy as np

def hex_int(x):
    return int(x, 16)

rooms = np.genfromtxt("map.csv", delimiter=",", dtype=hex_int, encoding="utf-8").flatten()

print(rooms)