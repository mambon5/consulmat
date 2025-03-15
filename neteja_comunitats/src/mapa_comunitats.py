import pandas as pd
import folium

# Carregar el CSV
df = pd.read_csv("input/Comunidades_coords.csv")  # Substitueix amb el teu fitxer

# Crear un mapa centrat en el primer punt
m = folium.Map(location=[df.iloc[0][2], df.iloc[0][3]], zoom_start=12)

# Afegir els punts al mapa
for _, row in df.iterrows():
    folium.Marker(
        location=[row[2], row[3]],
        popup=f'ID: {row[0]}<br>Direcció: {row[1]}',
        tooltip=row[1]
    ).add_to(m)

# Guardar el mapa en un fitxer
m.save("mapa.html")
print("Mapa generat: obre 'mapa.html' en el navegador.")
