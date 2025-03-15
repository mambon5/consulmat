import pandas as pd
import folium
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from lightgbm import LGBMClassifier


# ---------- 1. Carregar dades ----------
df = pd.read_csv("input/Comunidades_coords_capçal.csv")  # Substitueix amb el nom correcte
X = df[["lat", "lon"]].values  # Latitud i longitud

# ---------- 2. Agrupar amb K-Means ----------
num_clusters = 8  # Pots ajustar aquest valor segons les comunitats
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)


# ---------- 2.1. Visualitzar amb Folium ----------
m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=9.5)

colors = ["red", "blue", "green", "purple", "orange","black","yellow","brown"]  # Colors per als grups
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=colors[row["cluster"] % len(colors)],
        fill=True,
        fill_color=colors[row["cluster"] % len(colors)],
        popup=f'ID: {row["id"]}<br>Cluster: {row["cluster"]}',
        tooltip=row["adreça"]
    ).add_to(m)

# Guardar el mapa
m.save("mapa_clusters.html")
print("Mapa generat: obre 'mapa_clusters.html' en el navegador.")

# podriem posar-ho com a criteri per seguir tallant, que talla si n>50 elements
# ---------- 3. Entrenar Random Forest que no pot posar n maxim de elements per fulla ----------
X_train, X_test, y_train, y_test = train_test_split(X, df["cluster"], test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42, min_samples_leaf=8)
rf.fit(X_train, y_train)

# ---------- 3. Entrenar Random Forest més flexible ----------
# rf = LGBMClassifier(
#     min_child_samples=6,  # Mínim 5 mostres per fulla
#     num_leaves=50,       # Màxim 50 fulles
#     n_estimators=100,
#     random_state=42,
#     max_bin=35
# )
# rf.fit(X_train, y_train)



# ---------- 4. Avaluar el model ----------
y_pred = rf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Precisió del model: {acc:.2f}")

# Colors per als resultats de Random Forest
colors_rf = ["red", "black", "cyan", "blue", "magenta", "yellowgreen", "indigo", "salmon","brown", "yellow", "green"]

# Predir els clústers amb Random Forest
df["rf_cluster"] = rf.predict(X)

# Afegir els punts basats en les prediccions de Random Forest
m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=9.5)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=colors_rf[row["rf_cluster"] % len(colors_rf)],
        fill=True,
        fill_color=colors_rf[row["rf_cluster"] % len(colors_rf)],
        popup=f'ID: {row["id"]}<br>Cluster RF: {row["rf_cluster"]}',
        tooltip=row["adreça"]
    ).add_to(m)


# Guardar el mapa
m.save("mapa_rf.html")
print("Mapa generat: obre 'mapa_rf.html' en el navegador.")
df.to_csv("dades_clusteritzades.csv", index=False)
print("Fitxer 'dades_clusteritzades.csv' creat!")



