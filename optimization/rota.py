#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""

Rota script takes in multiple arguements about a route with multiple destinations and
a designated start/end location to solve the traveling salesman problem(TSP) with 
start/end constraint via simulated annealing(SA).

The script differs from standard SA with the initial constraint of start/end destination. 
This constraint makes the search function less efficient since better solutions are disregarded.

Simulated annealing parameters:
-Initial temperature = starting point of temperature(T0)
-M & N values = iteration amount(MxN)
-Alpha value = cooling rate(alpha)


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import googlemaps
import random
from datetime import datetime

locations_length = int(input('Başlangıç noktası haricinde kaç lokasyona gidilecek?: '))
locationsX = []
locationsDummy = ["Emirgan Korusu","Turkcell Kucukyali","Kanyon","Orjin Maslak","Levent Loft"]

if locations_length == 0:
    locations = locationsDummy
    locations_init = locationsDummy[0]
else:
    locations_init = str(input('Başlangıç noktası: '))
    for i in range(locations_length):
        data = str(input('Müşteri lokasyonu {0}: '.format(i+1)))
        locationsX.append(data)
    locationsX.insert(0, locations_init)
    locations = locationsX

gmaps = googlemaps.Client(key='AIzaSyBFbrjZ60wcVQ3vil3BSh-dw4FjZsbC7R4')
now = datetime.now()

matrix_result = gmaps.distance_matrix(locations, locations, mode="driving", departure_time=now, region="tr")
matrix_size = len(matrix_result['rows'][0]['elements'])
matrix_list = []
matrix_array = []

for x in range(matrix_size):
    addresses = matrix_result['destination_addresses'][x]
    print('Müşteri {0}: {1}'.format(x,addresses))

def matrix_search (x,y):
    return matrix_result['rows'][x]['elements'][y]['distance']['value']

def matrix_legit (x,y):
    return matrix_result['rows'][x]['elements'][y]['status']

for i in range(matrix_size):
    for j in range(matrix_size):
        status = matrix_legit(i,j)
        if status != 'OK':
            print("Adres hatalı ->", locations[j])
            exit()
        result = matrix_search(i,j)
        matrix_list.append(result)        
        
matrix_array = np.array(matrix_list).reshape((matrix_size,matrix_size))
df = pd.DataFrame(matrix_array, columns=locations, index=locations)

X0 = locations
Distances = []
t = 0

for i in range(len(X0)-1):
    X1 = df.loc[X0[t],X0[t+1]]
    X11 = df.loc[X0[-1],X0[0]]
    Distances.append(X1)
    t = t+1
    
Distances.append(X11)
Travel_length = sum(Distances)

print("Girdiğiniz rota: ", locations)
print("Toplam mesafe: ", Travel_length/1000, " km.")

# Parameters
T0 = 20000
M = 2000
N = 50
Alpha = 0.95

# Main loop over M/N
for i in range(M):
    for j in range(N):
        Rand1 = np.random.randint(0,len(X0))
        Rand2 = np.random.randint(0,len(X0))
        while Rand1 == Rand2:
            Rand2 = np.random.randint(0,len(X0))
            
        Xtemp = []
        A1 = X0[Rand1]
        A2 = X0[Rand2]
        w = 0
        
        # swap 2 random cities
        for i in X0:
            if X0[w] == A1:
                Xtemp = np.append(Xtemp, A2)
            elif X0[w] == A2:
                Xtemp = np.append(Xtemp, A1)
            else:
                Xtemp = np.append(Xtemp, X0[w])
            w = w+1
            
        Xtemp = list(Xtemp)
        
        Distances_X0 = []
        t = 0
        
        for i in range(len(X0)-1):
            X1_1 = df.loc[X0[t],X0[t+1]]
            X11 = df.loc[X0[-1],X0[0]]
            Distances_X0.append(X1_1)
            t = t+1
            
        Distances_X0.append(X11)
        Len_X0 = sum(Distances_X0)
        
        Distances_Xtemp = []
        t = 0
        
        for i in range(len(Xtemp)-1):
            X1_2 = df.loc[Xtemp[t],Xtemp[t+1]]
            X11 = df.loc[Xtemp[-1],Xtemp[0]]
            Distances_Xtemp.append(X1_2)
            t = t+1
        
        Distances_Xtemp.append(X11)
        Len_Xtemp = sum(Distances_Xtemp)
        
        formula = 1 / (np.exp((Len_Xtemp-Len_X0)/T0))
        rand_num = np.random.rand()
        
        if Xtemp[0] == locations_init:
            if Len_Xtemp <= Len_X0:
                X0 = Xtemp
            elif rand_num <= formula:
                X0 = Xtemp
            else:
                X0 = X0

        T0 = Alpha * T0
        
#kisa_rota = X0
#kisa_rota.append(X0[0])

print("En kısa rota:", X0)
print("En kısa mesafe:", Len_X0/1000, " km.")
print("Rotanın kısalma oranı: ", "%.2f" % (((Travel_length/1000)-(Len_X0/1000))/(Travel_length/1000)*100), "%")