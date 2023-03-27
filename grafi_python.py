import numpy as np
import matplotlib.pyplot as plt
#stevilo_notranjih_tock_1,varianca_1
converters = {0: lambda s: float(s.strip('"'))}
data_1 = np.loadtxt('poligon_30.txt', skiprows=1,delimiter=';', converters=converters, usecols=[1,2,3])
data_2 = np.loadtxt('n_kotnik_30.txt', skiprows=1,delimiter=';', converters=converters, usecols=[1,2,3])
data_3 = np.loadtxt('kroznica_30.txt', skiprows=1,delimiter=';', converters=converters, usecols=[1,2,3])

stevilo_nt_1 = []
povprecje_1 = []
varianca_1 = []
for i in range(len(data_1)):
    stevilo_nt_1.append(data_1[i][0])
    povprecje_1.append(data_1[i][1])
    varianca_1.append(data_1[i][2])

stevilo_nt_2 = []
povprecje_2 = []
varianca_2 = []
for i in range(len(data_2)):
    stevilo_nt_2.append(data_2[i][0])
    povprecje_2.append(data_2[i][1])
    varianca_2.append(data_2[i][2])

stevilo_nt_3 = []
povprecje_3 = []
varianca_3 = []
for i in range(len(data_3)):
    stevilo_nt_3.append(data_3[i][0])
    povprecje_3.append(data_3[i][1])
    varianca_3.append(data_3[i][2])


fig, ax = plt.subplots(figsize=(7,5))

ax.plot(stevilo_nt_1,varianca_1,'-')
ax.plot(stevilo_nt_2,varianca_2,'-')
ax.plot(stevilo_nt_3,varianca_3,'-')

ax.set_xlabel("število notranjih točk")
ax.set_ylabel("varianca")
ax.legend(['poligon', 'n-kotnik', 'krožnica'])

plt.show()

fig, ax = plt.subplots(figsize=(7,5))

ax.plot(stevilo_nt_1,povprecje_1,'-')
ax.plot(stevilo_nt_2,povprecje_2,'-')
ax.plot(stevilo_nt_3,povprecje_3,'-')

ax.set_xlabel("število notranjih točk")
ax.set_ylabel("čas izvajanja algoritma")
ax.legend(['poligon', 'n-kotnik', 'krožnica'])

plt.show()

