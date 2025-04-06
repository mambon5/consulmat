import folium

# Funció per llegir el fitxer
def llegir_fitxer(nom_fitxer):
    comunitats_per_dia = {
        'Dilluns': [],
        'Dimarts': [],
        'Dimecres': [],
        'Dijous': [],
        'Divendres': []
    }

    latitudes = []
    longitudes = []

    with open(nom_fitxer, 'r') as fitxer:
        linies = fitxer.readlines()
        linies = [linia.strip() for linia in linies if linia.strip()]  # Eliminar línies buides

        # Processar les línies de les comunitats per dia
        for i in range(5):
            dia = linies[i].split(":")[0].strip()  # El nom del dia
            comunitats = list(map(int, linies[i].split(":")[1].strip().split()))  # Les comunitats
            comunitats_per_dia[dia] = comunitats

        # Processar les línies de latituds i longituds
        latitudes = list(map(float, linies[5].strip().split(" - ")))
        longitudes = list(map(float, linies[6].strip().split(" - ")))

    return comunitats_per_dia, latitudes, longitudes

# Funció per dibuixar els mapes
def dibuixar_mapes(latitudes, longitudes, comunitats_per_dia):
    # Iterar sobre cada dia per crear un mapa per dia
    for dia in comunitats_per_dia:
        # Crear el mapa centrant-lo al voltant de la primera latitud/longitud
        mapa = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=10)

        # Afegir els punts al mapa només per a aquest dia
        for comunitat in comunitats_per_dia[dia]:
            lat = latitudes[comunitat]
            lon = longitudes[comunitat]

            # Afegir un marcador per cada comunitat
            folium.Marker(location=[lat, lon], popup=f"Comunitat {comunitat}").add_to(mapa)

        # Desar el mapa per aquest dia en un fitxer HTML
        mapa.save(f'mapa_comunitats_{dia}.html')

# Llegir les dades des del fitxer
nom_fitxer = 'punts.txt'  # El nom del fitxer amb les dades
comunitats_per_dia, latitudes, longitudes = llegir_fitxer(nom_fitxer)

# Dibuixar els mapes per cada dia
dibuixar_mapes(latitudes, longitudes, comunitats_per_dia)
