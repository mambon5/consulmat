# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 16:53:19 2025

@author: ruthv
"""

from itertools import combinations

# Definir comunidades con sus frecuencias y horas de limpieza por día
comunidades = {
    "Comunidad A": {"frecuencia": 5, "horas segun dia": [2, 1, 3, 1, 1]},  # Lunes 2h, Jueves 1h
    "Comunidad B": {"frecuencia": 2, "horas segun dia": [2, 1]},  # Lunes 2h, Martes 1h
    "Comunidad C": {"frecuencia": 3, "horas segun dia": [2, 2, 2]},  # Lunes 2h, Miércoles 2h, Viernes 2h
    "Comunidad D": {"frecuencia": 4, "horas segun dia": [1, 2, 1, 3]},  # Lunes 1h, Martes 2h, etc.
    "Comunidad E": {"frecuencia": 6, "horas segun dia": [2, 2, 2, 2, 2, 2]},  # 6 días a la semana
    "Comunidad F": {"frecuencia": 1, "horas segun dia": [1.5]},  # Solo 1 día
}

# Días de la semana (solo Lunes a Viernes por defecto)
dias = ["L", "M", "X", "J", "V"]
dias_sabado = ["L", "M", "X", "J", "V", "S"]  # Cuando la frecuencia es 6, añadimos el sábado

# Según la frecuencia, se saben los días a asignar (6,5,3 son fijos; 1,2,4 a elegir según conveniencia)
dias_fijos = {
    6: dias_sabado,  # Solo una opción, incluye sábado
    5: dias,         # Solo una opción, L, M, X, J, V
    3: [["L", "X", "V"]],  # Asignación fija de L, X, V para frecuencia 3
    4: list(combinations(dias, 4)),  # Combinaciones de 4 días de lunes a viernes para frecuencia 4
    2: [["L", "J"], ["M", "V"]],  # Combinaciones fijas de 2 días de lunes a viernes para frecuencia 2
    1: list(combinations(dias, 1)),  # Combinaciones de 1 día de lunes a viernes para frecuencia 1
}

# Orden de asignación de frecuencias: 6, 5, 3, 2, 4, 1 (ESTO ES MUY IMPORTAANTE porque va a determinar las horas de trabajo de cada día)
orden_frecuencias = [6, 5, 3, 2, 4, 1]

# Diccionario para almacenar la asignación de días
asignaciones = {c: [] for c in comunidades}

# Carga horaria diaria inicializada en 0
carga_horaria = {d: 0 for d in dias_sabado}  # Incluyendo sábado para la carga horaria

# Asignar comunidades por el orden de prioridad de frecuencias
for frecuencia in orden_frecuencias: 
    # Filtrar comunidades de acuerdo a la frecuencia actual
    comunidades_frecuencia = [comunidad for comunidad, datos in comunidades.items() if datos["frecuencia"] == frecuencia]

    # Asignar los días para cada comunidad en esta frecuencia
    for comunidad in comunidades_frecuencia:
        datos = comunidades[comunidad]
        horas = datos["horas segun dia"] # Lista de horas según los días de limpieza

        if len(horas) != frecuencia:
            if len(horas) == 0: #Si horas está vacío, lo reemplaza por [0] * frecuencia, asegurando que tenga el tamaño correcto.
                print(f"⚠️ Advertencia en {comunidad}: La lista de horas está vacía, se asignará 0 horas.")
                horas = [0] * frecuencia  # Rellenamos con ceros para evitar que salte error # 
            else:
                raise ValueError(f"Error en {comunidad}: La cantidad de elementos en la lista de horas no coincide con la frecuencia de días de limpieza que tiene esa comunidad.")
      
        if frecuencia == 1:
            #Para frecuencia 1, elegimos el día con la mayor cantidad de horas
           # selecciona el día de la semana que maximiza la suma de: la carga horaria total ya acumulada en ese día y las horas asignadas a la comunidad en ese día.
            mejor_dia = max(dias, key=lambda d: horas[0]+ carga_horaria[d]) #carga_horaria[d] : cuántas horas de trabajo hay acumuladas en ese día d.
            asignaciones[comunidad] = [mejor_dia]
            carga_horaria[mejor_dia] += horas[0] # Solo hay un día, por eso, horas solo tiene un valor
            # horas[0] representa cuántas horas de limpieza tiene esa comunidad para el día que elijamos.
        

        elif frecuencia == 4:
            # Para frecuencia 4, seleccionamos la mejor combinación de 4 días
            mejor_combinacion = max(
                dias_fijos[4],
                key=lambda comb: sum(horas[i] + carga_horaria[d] for i, d in enumerate(comb))
            )

            # Guardamos la mejor combinación de días para esta comunidad
            asignaciones[comunidad] = mejor_combinacion
    
            # Actualizamos la carga horaria en cada día de la mejor combinación
            for i, d in enumerate(mejor_combinacion):
                carga_horaria[d] += horas[i]
                
        elif frecuencia == 5:
            mejor_combinacion = dias_fijos[5]  # Se usa directamente ["L", "M", "X", "J", "V"]

            # Guardamos la mejor combinación de días para esta comunidad
            asignaciones[comunidad] = mejor_combinacion
    
            # Actualizamos la carga horaria en cada día de la mejor combinación
            for i, d in enumerate(mejor_combinacion):
                carga_horaria[d] += horas[i]                

# Para poder guardar las comunidades que se asignan a cada día debemos crear un diccionario de las comunidades_por_dia y que dichas claves sean string por eso convertimos dias_fijos en str

# Convertir listas y tuplas a cadenas de texto en dias_fijos
dias_fijos_str = {k: [str(d) for d in v] for k, v in dias_fijos.items()}

# Diccionario para almacenar qué comunidades tienen asignado cada día
comunidades_por_dia = {d: [] for d in set(sum(dias_fijos_str.values(), []))}

# Registrar cada comunidad en los días que le corresponden
for comunidad, dias_asignados in asignaciones.items():
    if dias_asignados:  # Solo procesar si hay días asignados
        horas_asignadas = comunidades[comunidad]["horas segun dia"]  # Obtiene las horas de esa comunidad
        for i, d in enumerate(dias_asignados):
            comunidades_por_dia[str(d)].append(f"{comunidad} ({horas_asignadas[i]}h)")  # Convertir a cadena de texto

# Imprimir resultados
print("\nDías asignados a cada comunidad:")
for comunidad, dias in asignaciones.items():
    print(f"{comunidad}: {', '.join(dias)}")

# Carga horaria total por día (Lunes a Sábado), mostrando qué comunidades trabajan en cada día
print("\nComunidades asignadas por día y carga horaria total diaria:")
for d, h in carga_horaria.items():
    comunidades_en_este_dia = ", ".join(comunidades_por_dia[str(d)])
    print(f"{d}: {h} horas → {comunidades_en_este_dia}")