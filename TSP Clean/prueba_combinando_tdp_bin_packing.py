# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 00:57:42 2025

@author: ruthv
"""

import numpy as np
from itertools import combinations
from scipy.spatial.distance import cdist

# 1. Datos de las comunidades y sus coordenadas (Ejemplo de coordenadas)
comunidades = {
    "Comunidad A": {"frecuencia": 5, "horas segun dia": [2, 1, 3, 1, 1], "coordenadas": (0, 0)},  # Lunes 2h, Jueves 1h
    "Comunidad B": {"frecuencia": 2, "horas segun dia": [2, 1], "coordenadas": (2, 2)},  # Lunes 2h, Martes 1h
    "Comunidad C": {"frecuencia": 3, "horas segun dia": [2, 2, 2], "coordenadas": (4, 0)},  # Lunes 2h, Miércoles 2h, Viernes 2h
    "Comunidad D": {"frecuencia": 4, "horas segun dia": [1, 2, 1, 3], "coordenadas": (1, 3)},  # Lunes 1h, Martes 2h, etc.
    "Comunidad E": {"frecuencia": 6, "horas segun dia": [2, 2, 2, 2, 2, 2], "coordenadas": (5, 5)},  # 6 días a la semana
    "Comunidad F": {"frecuencia": 1, "horas segun dia": [1.5], "coordenadas": (3, 4)},  # Solo 1 día
}

# Coordenadas de las comunidades
coordenadas = np.array([comunidades[comunidad]["coordenadas"] for comunidad in comunidades])

# 2. Generar la matriz de distancias entre comunidades
distancia_matriz = cdist(coordenadas, coordenadas, metric='euclidean')

# 3. Bin Packing: Asignar días a las comunidades sin exceder las horas diarias
def bin_packing(dias_disponibles, horas):
    max_horas = 7.5  # Máxima carga horaria por día
    dias_asignados = []
    
    for i, horas_dia in enumerate(horas):
        if i >= len(dias_disponibles):  # Si tenemos más horas que días disponibles
            break
        
        dia = dias_disponibles[i]
        if carga_horaria[dia] + horas_dia <= max_horas:
            dias_asignados.append(dia)
            carga_horaria[dia] += horas_dia

    return dias_asignados

# 4. Resolver el TSP (Traveling Salesman Problem) para optimizar la asignación de días
def tsp(distancias):
    # Resolver el problema del TSP usando Nearest Neighbor o cualquier algoritmo adecuado
    num_comunidades = len(distancias)
    visitado = [False] * num_comunidades
    recorrido = [0]  # Empezamos desde la comunidad 0
    visitado[0] = True
    
    for _ in range(num_comunidades - 1):
        ultimo = recorrido[-1]
        min_distancia = float('inf')
        siguiente_comunidad = -1
        
        for j in range(num_comunidades):
            if not visitado[j] and distancias[ultimo][j] < min_distancia:
                min_distancia = distancias[ultimo][j]
                siguiente_comunidad = j
        
        recorrido.append(siguiente_comunidad)
        visitado[siguiente_comunidad] = True
    
    return recorrido

# Resolver el TSP para obtener el orden óptimo de comunidades
orden_optimo = tsp(distancia_matriz)

# 5. Asignación final de comunidades a días con TSP
asignaciones_optimizadas = []
for comunidad_idx in orden_optimo:
    comunidad = list(comunidades.keys())[comunidad_idx]
    dias_asignados = bin_packing(dias_fijos[comunidades[comunidad]["frecuencia"]], comunidades[comunidad]["horas segun dia"])
    asignaciones_optimizadas.append((comunidad, dias_asignados))

# 6. Imprimir resultados
print("Asignación final de comunidades a días (con optimización TSP):")
for comunidad, dias in asignaciones_optimizadas:
    print(f"{comunidad} -> {dias}")
