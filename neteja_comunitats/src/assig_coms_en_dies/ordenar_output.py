# Nom del fitxer d'entrada
INPUT_FILE = "dies_assignats_lp.txt"
OUTPUT_FILE = "dies_assignats.txt"

# Mapa de dies de la setmana
dies_setmana = {
    0: "Dilluns",
    1: "Dimarts",
    2: "Dimecres",
    3: "Dijous",
    4: "Divendres",
    5: "Dissabte",
    6: "Diumenge"
}

# Diccionari per emmagatzemar les comunitats per dia
neteja_per_dia = {dia: [] for dia in dies_setmana.values()}

# Llegeix i processa el fitxer
with open(INPUT_FILE, "r") as file:
    for linia in file:
        if linia.startswith("x"):
            part = linia.split()[0]  # ex: x0,2
            dia_str, comunitat_str = part[1:].split(",")
            dia = int(dia_str)
            comunitat = comunitat_str
            nom_dia = dies_setmana.get(dia)
            if nom_dia:
                neteja_per_dia[nom_dia].append(comunitat)

# Escriu el resultat al fitxer de sortida
with open(OUTPUT_FILE, "w") as out_file:
    for dia, comunitats in neteja_per_dia.items():
        if comunitats:
            comunitats_str = ",".join(comunitats)
            out_file.write(f"{dia}: {comunitats_str}\n")