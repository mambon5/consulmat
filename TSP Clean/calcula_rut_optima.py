# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:46:27 2025

@author: ruthv
"""

import numpy as np
from itertools import permutations

# Definir la matriz de distancias (en km) entre las comunidades
distancias = np.array([
    [0, 10, 15, 30],  # Distancias desde A
    [10, 0, 12, 5],   # Distancias desde B
    [15, 12, 0, 8],   # Distancias desde C
    [30, 5, 8, 0],    # Distancias desde D
])

# Comunidades
comunidades = ["Comunidad A", "Comunidad B", "Comunidad C", "Comunidad D"]

# Función para calcular la distancia total de un recorrido
def calcular_distancia(ruta, distancias):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += distancias[ruta[i], ruta[i + 1]]
    return distancia_total

# Función para encontrar las rutas con la distancia mínima
def rutas_optimas(distancias):
    n = len(distancias)
    indices = list(range(n))
    min_distancia = float('inf')
    rutas = []

    # Generar todas las posibles permutaciones de las comunidades
    for ruta in permutations(indices):
        # Calcular la distancia total para cada ruta
        distancia_total = calcular_distancia(ruta, distancias)
        
        # Si encontramos una nueva ruta con menor distancia, la almacenamos
        if distancia_total < min_distancia:
            min_distancia = distancia_total
            rutas = [ruta]  # Nueva lista de rutas con la nueva distancia mínima
        # Si la distancia es la misma que la mínima, la añadimos a las rutas. Puede ser que haya más de una óptima, con una distancia de desplazamiento total igual
        elif distancia_total == min_distancia:
            rutas.append(ruta)

    return rutas, min_distancia

# Ejecutar la función y obtener las rutas con la distancia mínima
rutas, distancia_minima = rutas_optimas(distancias)

# Mostrar las rutas y la distancia mínima
print(f"Distancia mínima: {distancia_minima} km\n")
print("Rutas óptimas:")
for ruta in rutas:
    recorrido = " -> ".join(comunidades[i] for i in ruta)
    print(f"{recorrido} -> Fin del recorrido")
