# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 21:42:48 2025

@author: ruthv
"""

comunidades_info = [
    {"comunidad": "Comunidad A", "limpieza_por_semana": 3, "horas_por_limpieza": 1.5},
    {"comunidad": "Comunidad B", "limpieza_por_semana": 2, "horas_por_limpieza": 2},
    {"comunidad": "Comunidad C", "limpieza_por_semana": 1, "horas_por_limpieza": 1},
    {"comunidad": "Comunidad D", "limpieza_por_semana": 4, "horas_por_limpieza": 1.2}
]
#lista de diccionarios 

print(comunidades_info) # Mostrar todo
print(comunidades_info[0]) # Mostrar una determinada 
print(comunidades_info[0]["comunidad"])  # comunidad
print(comunidades_info[0]["limpieza_por_semana"])  # comunidad
print(comunidades_info[0]["horas_por_limpieza"])  

trabajadores = ["Trabajador 1","Trabajador 2"] 
trabajador_1 = trabajadores[0]
