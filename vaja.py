
import itertools
import sys
import random
import matplotlib.pyplot as plt
import random
from shapely.affinity import affine_transform
from shapely.geometry import Point, Polygon
from shapely.ops import triangulate
import numpy as np
from functools import reduce
import operator
from itertools import chain, combinations
import random
import math




num_vertices = 10  # number of vertices in the polygon
min_coord = 0  # minimum value for x and y coordinates
max_coord = 100  # maximum value for x and y coordinates

# generate a list of random x coordinates
x_coords = [random.uniform(min_coord, max_coord) for _ in range(num_vertices)]

# generate a list of random y coordinates
y_coords = [random.uniform(min_coord, max_coord) for _ in range(num_vertices)]

# zip the x and y coordinates and sort them based on the angle they make with the x-axis
sorted_coords = sorted(zip(x_coords, y_coords), key=lambda coord: math.atan2(coord[1], coord[0]))

# unzip the sorted coordinates
x_coords, y_coords = zip(*sorted_coords)

# create the convex hull
#hull = ConvexHull(list(zip(x_coords, y_coords)))