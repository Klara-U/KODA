import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time 


def random_tocka_na_krogu(radij):
    # Funkcija vrne koordinate random točke na krožnici z nekim radijem.
    phi_tocke = random.uniform(0, 2*math.pi)
    
    return (radij*math.cos(phi_tocke), radij*math.sin(phi_tocke))

def random_tocke_na_krogu(radij, stevilo_tock):
    sez = []
    for x in range(stevilo_tock):
        sez.append(random_tocka_na_krogu(radij))
    return sez

def random_tocka_v_krogu(radij):
    # Funkcija vrne koordinate random točke v krogu z nekim radijem.
    phi_tocke = random.uniform(0, 2*math.pi)
    
    radij_tocke = math.sqrt(random.uniform(0,radij**2))
    return (radij_tocke*math.cos(phi_tocke), radij_tocke*math.sin(phi_tocke))

def random_tocke_v_krogu(radij, stevilo_tock):
    sez = []
    for x in range(stevilo_tock):
        sez.append(random_tocka_v_krogu(radij))
    return sez

if __name__ == "__main__":
    zacetni_cas = time.perf_counter()
    n = 7
    k = 5
    # Določimo polmer
    radij = random.random() * 1000
    # Določimo točke na in v krožnici s pomočjo prej definiranih funkcij
    zunanje, notranje = random_tocke_na_krogu(radij,n), random_tocke_v_krogu(radij, k)
    # Pripravimo krožnico, da jo bomo lahko narisali
    theta = np.linspace(0, 2*np.pi, 1000)
    a, b = radij * np.cos(theta), radij * np.sin(theta)
    # Narišemo krožnico
    plt.plot(a, b, linestyle='-', linewidth=2)
    # Narišemo točke na krožnici
    plt.plot([p[0] for p in zunanje], [p[1] for p in zunanje],'o')
    # Narišemo točke v krogu
    plt.plot([p[0] for p in notranje], [p[1] for p in notranje],marker="o", markersize=5)
    plt.show()
    print("Zunanje tocke", zunanje)
    print("Notranje tocke", notranje)
    koncni_cas = time.perf_counter()
    cas_izvajanja = koncni_cas - zacetni_cas
    print(cas_izvajanja)