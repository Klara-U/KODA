import sys
import math
import random
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import numpy as np
from functools import reduce
import operator
from itertools import chain, combinations
import time
import csv

#=========================================================
# GENERIRANJE RANDOM KONVEKSNEGA POLIGONA
#=========================================================
# apliciramo Pavel Valtrov algoritem za generiranje random konveksnega poligona
# pomožna funkcija, ki random razdeli seznam na dva seznama
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
    # razporedimo vektorje glede na kot
    vectors.sort(key=lambda v: math.atan2(v[1], v[0]))
    # nastavimo začetek prvega vektorja v izhodišče
    points = [(0, 0)]
    # dodamo vektorje, da tvorijo poligon
    for v in vectors:
        points.append((points[-1][0] + v[0], points[-1][1] + v[1]))
    # premaknemo poligon na originalne minimalne in maksimalne koordinate
    xmin = min([p[0] for p in points])
    ymin = min([p[1] for p in points])
    dx = a1 - xmin
    dy = b1 - ymin
    points = [(p[0]+dx, p[1]+dy) for p in points]
    # shranimo točke po vrsti kot si sledijo v smeri urinega kazalca
    # izračuna center tock 
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points), [len(points)] * 2))
    outer = sorted(points, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
    # dobimo urejene točke poligona
    return outer

#=========================================================
# GENERIRANJE PRAVILNEGA N-KOTNIKA
#=========================================================

pravilni_n_kotnik = (lambda n: (lambda m=__import__("math"), rn=__import__("random"): (r:=rn.random() * 1000) and 
                    (phi0:=rn.random() * 2 * m.pi) and (phi:=(2 * m.pi)/n) and [(r * m.cos(phi0 + i * phi), r * m.sin(phi0 + i * phi)) for i in range(n)])())

#=========================================================
# GENERIRANJE NAKLJUČNIH TOČK NA KROŽNICI
#=========================================================

def random_tocka_na_krogu(radij):
    # Funkcija vrne koordinate random točke na krožnici z nekim radijem.
    phi_tocke = random.uniform(0, 2*math.pi)
    
    return (radij*math.cos(phi_tocke), radij*math.sin(phi_tocke))

def random_tocke_na_krogu(radij, stevilo_tock):
    sez = []
    for x in range(stevilo_tock):
        sez.append(random_tocka_na_krogu(radij))
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), sez), [len(sez)] * 2))
    outer = sorted(sez, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
    # dobimo urejene točke poligona
    return outer


#=========================================================
# GENERIRANJE RANDOM TOČK ZNOTRAJ POLIGONA
#=========================================================
# funkcija, ki random izbere k tock znotraj poligona
def random_points_in_polygon(polygon, k):
    # definiramo meje poligona, da imamo najmanjši pravokotnik, ki vsebuje naš poligon
    min_x, min_y, max_x, max_y = polygon.bounds
    # naredimo prazen seznam 
    tocke = []
    # dokler točk v seznamu ni k, generiramo random točke za katere preverimo, če so znotraj poligona
    # če so točke noter, jih dodamo v seznam, sicer gremo dalje
    while len(tocke)<k:
        random_point = Point([random.uniform(min_x,max_x),random.uniform(min_y, max_y)])
        if (random_point.within(polygon)):
            tocke.append(random_point)
    # tocke smo dobili v obliki Point, zato jih spremenimo v želeno obliko   
    notranje_tocke = []
    for tocka in tocke:
        x = tocka.x
        y = tocka.y
        notranje_tocke.append((x,y))
    # dobimo seznam notranjih tock 
    return notranje_tocke

#=========================================================
# POMOŽNE FUNKCIJE
#=========================================================
# funkcija, ki izračuna razdaljo med točkama v evklidski ravnini
def dist(a,b):
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)

# vrne vse mozne podmnožice indeksov elementov
def vse_podmnozice(n):
    return list(chain.from_iterable(combinations(list(range(n)),r) for r in range(n+1)))


#=========================================================
# ALGORITEM ZA REŠITEV TSP Z DINAMIČNIM PROGRAMIRANJEM
#=========================================================
# slovar z vsemi vmesnimi vrednostmi, kjuči so trojice (i,S,r), vrednosti so pari dolžin do r in prejšnjih tocka
# tu jih nastavimo na [0,None] oz. [inf, None]
def DP_slovar(outer, inner):
    # seznam vseh podmnožic indeksov notranjih tock
    subS = list(vse_podmnozice(len(inner)))
    memo = {}
    # dodamo trojice, najprej za i, ki gre po indeksih zunanjih tock
    for i in range(len(outer)):
        # dodamo podmnozice notranjih na mesto S in zunanje na mesto r
        for sub in subS:
            memo[i,sub, i] = [math.inf, None]
        # dodamo notranje na mesto r 
        for r in range(len(inner)):
            b = len(outer) + r
            # dodamo na mesto S vse podmnožice, ki ne vsebujejo trenutne r
            for sub in subS:
                if r not in sub:
                    continue
                else:
                    memo[i,sub, b] = [0, None]
    # nastavimo začetni pogoj
    memo[0, (), 0] = [0, None]
    # vrnemo slovar in podmnožice
    return memo, subS

# izračunamo vse vmesne poti in koncno pot (dolzino in tocke na poti)
def DP_pot(outer, inner):
    f, subs = DP_slovar(outer, inner)
    for i in range(len(outer)):
        if i != 0:
            # računa vrednosti slovarja, če je r zunanja točka
            for s in subs:
                f[i, s, i] = [math.inf, None]
                for t in s:
                    # primerjamo poti, ker je bila prejsnja tocka notranja
                    temp = f[i-1, s, len(outer) + t][0] + dist(outer[i], inner[t])
                    if temp < f[i, s, i][0]:
                        f[i, s, i] = [temp, [i-1, s, len(outer) + t]]
                # primerjamo še prejsnji najboljši izid z izidom, če je prejsnja notranja
                temp = f[i-1, s, i-1][0] + dist(outer[i-1], outer[i])
                if temp < f[i, s, i][0]:
                    f[i, s, i] = [temp, [i-1, s, i-1]]
                #print((i, s, i), f[i, s, i])

    # računa če je na mestu r notranja tocka
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
                #print((i, s, len(outer) + b), f[i, s, len(outer) + b])

    #koncno resitev nastavimo na neskoncno
    final = [math.inf, None]
    #izberemo najkrajsi obhod, če je zadnja točka notranja tocka
    for t in subs[-1]:
        temp = f[i, subs[-1], len(outer) + t][0] + dist(outer[0], inner[t])
        if temp < final[0]:
            final = [temp, [i, subs[-1], len(outer) + t]]
    #primerjamo najkrajši obhod iz prejšnjih vrstic, z obhodom, ko je zadnja tocka zunanja
    temp = f[i, subs[-1], i][0] + dist(outer[0], outer[i])
    if temp < final[0]:
        final = [temp, [i, subs[-1], i]]
    #predzadnja točka
    prev = final[1]
    #pot nastavimo na 0
    pot = [0]
    # dodajamo zadnje točke v vrsti
    while prev:
        pot.append(prev[2])
        prev = f[tuple(prev)][1]

    pot.reverse()

    vse = outer + inner
    pot_tocke = [vse[i] for i in pot]
    # vrne dolzino najkrajšega obhoda in zaporedje, kako si sledijo točke
    return final, pot_tocke



if __name__ == "__main__":
    rezultati = []
    for n in range(10,11, 10):
        for k in range(1):
            vrstica = [n,k]
            for j in range(1):
                n = 20
                k = 10

                # PODATKI
                podatki = 3

                if podatki == 1:
                    # NAKLJUČNO GENERIRAN KONVEKSEN POLIGON
                    outer = get_xyq(n)
                    polygon = Polygon(outer)
                    notranje_tocke = random_points_in_polygon(polygon,k)
                elif podatki == 2:
                    # PRAVILNI N-KOTNIK
                    outer = pravilni_n_kotnik(n)
                    outer = outer + outer[:1]
                    polygon_1 = Polygon(outer)
                    notranje_tocke = random_points_in_polygon(polygon_1, k)
                else:
                    #KROŽNICA
                    radij = random.random() * 1000
                    outer = random_tocke_na_krogu(radij,n)
                    polygon = Polygon(outer)
                    notranje_tocke = random_points_in_polygon(polygon, k)
                
                #ALGORITEM
                zacetni_cas = time.perf_counter()
                dolzina, pot = DP_pot(outer,notranje_tocke)
                koncni_cas = time.perf_counter()
                cas_izvajanja = round(koncni_cas - zacetni_cas, 7)
                
                #plotanje
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.plot([p[0] for p in pot], [p[1] for p in pot],"-", color='black')
                ax.plot([p[0] for p in outer], [p[1] for p in outer],"o", markersize=6)
                ax.plot([p[0] for p in notranje_tocke], [p[1] for p in notranje_tocke],"o", markersize=6)
                #ax.set_xlim([0,1])
                #ax.set_ylim([0,1])
                plt.show()
                vrstica.append(cas_izvajanja)
                print(cas_izvajanja)
            rezultati.append(vrstica)
            

    #with open('rezultati', 'w', newline='') as detoteka_csv:
    #    writer = csv.writer(detoteka_csv)
    #    writer.writerows(rezultati)

    

    
    

    





