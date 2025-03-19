# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 23:57:55 2025

@author: ruthv
"""

from itertools import combinations
from collections import defaultdict

# Definir comunidades con sus frecuencias y horas de limpieza por día
comunidades = {
    "Comunidad A": {"frecuencia": 5, "horas segun dia": [2, 1, 3, 1, 1]},
    "Comunidad B": {"frecuencia": 2, "horas segun dia": [2, 1]},
    "Comunidad C": {"frecuencia": 3, "horas segun dia": [2, 2, 2]},
    "Comunidad D": {"frecuencia": 4, "horas segun dia": [1, 2, 1, 3]},
    "Comunidad E": {"frecuencia": 6, "horas segun dia": [2, 2, 2, 2, 2, 2]},
    "Comunidad F": {"frecuencia": 1, "horas segun dia": [8]},
}

dias = ["L", "M", "X", "J", "V"]
dias_sabado = ["L", "M", "X", "J", "V", "S"]

dias_fijos = {
    6: dias_sabado,
    5: dias,
    3: [["L", "X", "V"]],
    4: list(combinations(dias, 4)),
    2: [["L", "J"], ["M", "V"]],
    1: list(combinations(dias, 1)),
}

orden_frecuencias = [6, 5, 3, 2, 4, 1]

asignaciones = {c: [] for c in comunidades}
carga_horaria = {d: 0 for d in dias_sabado}
trabajadores_por_dia = {d: defaultdict(float) for d in dias_sabado}
asignacion_trabajadores = defaultdict(dict)

trabajador_id = 1  # Contador de trabajadores
comunidades_asignadas = {}  # Diccionario para almacenar a qué trabajador pertenece cada comunidad

for frecuencia in orden_frecuencias:
    comunidades_frecuencia = [c for c, datos in comunidades.items() if datos["frecuencia"] == frecuencia]
    for comunidad in comunidades_frecuencia:
        datos = comunidades[comunidad]
        horas = datos["horas segun dia"]
        
        if len(horas) != frecuencia:
            raise ValueError(f"Error en {comunidad}: Lista de horas no coincide con la frecuencia.")

        if frecuencia in [1, 2, 4]:
            mejor_opcion = min(dias_fijos[frecuencia], key=lambda comb: sum(horas[i] + carga_horaria[d] for i, d in enumerate(comb)))
        else:
            mejor_opcion = dias_fijos[frecuencia][0]

        asignaciones[comunidad] = mejor_opcion
        
        trabajador_asignado = None
        if comunidad in comunidades_asignadas:
            trabajador_asignado = comunidades_asignadas[comunidad]
        else:
            for t in range(1, trabajador_id + 1):
                if all(trabajadores_por_dia[d][t] + horas[i] <= 7.5 for i, d in enumerate(mejor_opcion)):
                    trabajador_asignado = t
                    break
            if trabajador_asignado is None:
                trabajador_asignado = trabajador_id
                trabajador_id += 1
            comunidades_asignadas[comunidad] = trabajador_asignado

        for i, d in enumerate(mejor_opcion):
            if trabajadores_por_dia[d][trabajador_asignado] + horas[i] > 7.5 + 1e-9:
                raise ValueError(f"Error: El trabajador {trabajador_asignado} supera las 7.5 horas el día {d}.")
            carga_horaria[d] += horas[i]
            trabajadores_por_dia[d][trabajador_asignado] += horas[i]
            asignacion_trabajadores[d].setdefault(trabajador_asignado, []).append((comunidad, horas[i]))

# Mostrar asignaciones
for dia in dias_sabado:
    print(f"\nDía {dia}:")
    for trabajador, comunidades in asignacion_trabajadores[dia].items():
        print(f"  Trabajador {trabajador}: {comunidades}")
