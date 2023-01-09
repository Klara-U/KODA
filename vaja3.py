
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
import math

# funkcija, ki izračuna razdaljo med točkama v evklidski ravnini
outer = [(0,0),(0,3),(3,3),(3,0)]

inner = [(1,1),(1,2)]


def vse_podmnozice(n):
    return list(chain.from_iterable(combinations(list(range(n)),r) for r in range(n+1)))


def dist(a,b):
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)

def DP_drevo(outer, inner):
    subS = list(vse_podmnozice(len(inner)))
    # slovar z vsemi vmesnimi vrednostmi, kjuči so trojice (i,r,S), vrednosti bomo kasneje nastavili na dolžino poti
    memo = {}
    for i in range(len(outer)):
        for sub in subS:
            memo[i,sub, i] = [math.inf, None]
        for r in range(len(inner)):
            b = len(outer) + r
            for sub in subS:
                if r not in sub:
                    continue
                else:
                    memo[i,sub, b] = [0, None]
    memo[0, (), 0] = [0, None]
    return memo, subS

f, subs = DP_drevo(outer, inner)
print(f)

for i in range(len(outer)):
    if i != 0:
        # računa A
        for s in subs:
            f[i, s, i] = [math.inf, None]
            for t in s:
                temp = f[i-1, s, len(outer) + t][0] + dist(outer[i], inner[t])
                if temp < f[i, s, i][0]:
                    f[i, s, i] = [temp, [i-1, s, len(outer) + t]]

            temp = f[i-1, s, i-1][0] + dist(outer[i-1], outer[i])
            if temp < f[i, s, i][0]:
                f[i, s, i] = [temp, [i-1, s, i-1]]

            print((i, s, i), f[i, s, i])

    # računa B
    for s in subs:
        for b in range(len(inner)):
            if b not in s:
                continue

            f[i, s, len(outer) + b] = [math.inf, None]
            novi_s = tuple(x for x in s if x != b)
            for t in novi_s:
                temp = f[i, novi_s, len(outer) + t][0] + dist(inner[b], inner[t])
                if temp < f[i, s, len(outer) + b][0]:
                    f[i, s, len(outer) + b] = [temp, [i, novi_s, len(outer) + t]]
            temp = f[i, novi_s, i][0] + dist(inner[b], outer[i])
            if temp < f[i, s, len(outer) + b][0]:
                f[i, s, len(outer) + b] = [temp, [i, novi_s, i]]
            print((i, s, len(outer) + b), f[i, s, len(outer) + b])


final = [math.inf, None]
for t in subs[-1]:
    temp = f[i, subs[-1], len(outer) + t][0] + dist(outer[0], inner[t])
    if temp < final[0]:
        final = [temp, [i, subs[-1], len(outer) + t]]

temp = f[i, subs[-1], i][0] + dist(outer[0], outer[i])
if temp < final[0]:
    final = [temp, [i, subs[-1], i]]

print(final)
prev = final[1]
pot = [0]
while prev:
    pot.append(prev[2])
    prev = f[tuple(prev)][1]

pot.reverse()
print(pot)

vse = outer + inner
pot_tocke = [vse[i] for i in pot]
print(pot_tocke)