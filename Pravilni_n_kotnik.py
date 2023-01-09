import sys
import math
import random
import matplotlib.pyplot as plt
import random
from shapely.affinity import affine_transform
from shapely.geometry import Point, Polygon
from shapely.ops import triangulate
import numpy as np
from functools import reduce
import operator
import time


# vmesna funkcija, ki random razdeli seznam na dva seznama
def random_partition(a):
    b = list()
    c = list()
    for i in range(len(a)):
        if random.randrange(2):
            b.append(a[i])
        else:
            c.append(a[i])
    return b,c

# funkcija, ki nam generira random seznam n stevil in jih uredi
def get_deltas(n):
    # generiramo n stevil
    de = [random.random() for _ in range(n)]
    # jih uredimo
    de.sort()
    #razdelimo brez prvega in zadnjega z random particijo na dva seznama
    dep, dem = random_partition(de[1:-1])
    # drugemu seznamu obrnemo vrstni red
    dem.reverse()
    # seznam = prvi element + prva particija + zadnji + druga particija + prvi
    des = [de[0]] + dep + [de[-1]] + dem + [de[0]]
    # naredimo vektor razdalj med elementi
    deltas = [des[i] - des[i-1] for i in range(1, len(des))]
    # vrnemo vektor razdalj, prvi in zadnji element
    return deltas, (de[0], de[-1])

def get_xyq(n):
    # dobimo razdalje, x, y, ter prve in zadnje koordinate
    x, (a1, a2) = get_deltas(n)
    y, (b1, b2) = get_deltas(n)
    # random zmesamo y
    random.shuffle(y)
    # damo skupaj razdalje, da dobimo usmerjene vektorje v ravnini
    vectors = [(x[i], y[i]) for i in range(n)]
    vectors.sort(key=lambda v: math.atan2(v[1], v[0]))
    points = [(0, 0)]
    for v in vectors:
        points.append((points[-1][0] + v[0], points[-1][1] + v[1]))
    xmin = min([p[0] for p in points])
    ymin = min([p[1] for p in points])
    dx = a1 - xmin
    dy = b1 - ymin
    points = [(p[0]+dx, p[1]+dy) for p in points]
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points), [len(points)] * 2))
    outer = sorted(points, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
    return outer

# funkcija, ki random izbere k tock znotraj poligona
def random_points_in_polygon(polygon, k):
    min_x, min_y, max_x, max_y = polygon.bounds
    tocke = []
    while len(tocke)<k:
        random_point = Point([random.uniform(min_x,max_x),random.uniform(min_y, max_y)])
        if (random_point.within(polygon)):
            tocke.append(random_point)   
    notranje_tocke = []
    for tocka in tocke:
        x = tocka.x
        y = tocka.y
        notranje_tocke.append((x,y))
    return notranje_tocke


# funkcija, ki izračuna razdaljo med točkama v evklidski ravnini
def dist(a,b):
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)
    

#funkcija, ki poda naključne koordinate točk za poljubno izbran pravilni n-kotnik
pravilni_n_kotnik = (lambda n: (lambda m=__import__("math"), rn=__import__("random"): (r:=rn.random() * 1000) and 
                    (phi0:=rn.random() * 2 * m.pi) and (phi:=(2 * m.pi)/n) and [(r * m.cos(phi0 + i * phi), r * m.sin(phi0 + i * phi)) for i in range(n)])())


if __name__ == "__main__":
    zacetni_cas = time.perf_counter()
    n = 10
    k = 10
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    outer = pravilni_n_kotnik(n)
    outer = outer + outer[:1]
    polygon_1 = Polygon(outer)
    notranje_tocke_1 = random_points_in_polygon(polygon_1, k)
    plt.plot([p[0] for p in outer], [p[1] for p in outer],marker="o", markersize=5)
    plt.plot([p[0] for p in notranje_tocke_1], [p[1] for p in notranje_tocke_1],marker="o", markersize=5)
    plt.show()
    print("Zunanje tocke", outer)
    print("Notranje tocke", notranje_tocke_1)
    koncni_cas = time.perf_counter()
    cas_izvajanja = koncni_cas - zacetni_cas
    print(cas_izvajanja)