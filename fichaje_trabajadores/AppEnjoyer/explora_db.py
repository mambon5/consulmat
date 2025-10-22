import pymysql
import os
from dotenv import load_dotenv
from tabulate import tabulate  # 👈 Per formatar taules

# Carregar variables del .env
load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)
cursor = conn.cursor()

# Llistar taules
cursor.execute("SHOW TABLES;")
taules = [t[0] for t in cursor.fetchall()]

print("\n📊 Taules disponibles a la base de dades:\n")
for i, taula in enumerate(taules, 1):
    print(f"{i}. {taula}")

print("\n──────────────────────────────────────────────")

for taula in taules:
    print(f"\n📁 Taula: {taula}")
    print("──────────────────────────────────────────────")

    # Mostrar columnes
    cursor.execute(f"DESCRIBE {taula};")
    columnes = [c[0] for c in cursor.fetchall()]
    # print("🧩 Columnes:", ", ".join(columnes))

    # Mostrar files
    cursor.execute(f"SELECT * FROM {taula} LIMIT 5;")
    files = cursor.fetchall()
    if files:
        print("\n📄 Primeres 5 files:")
        print(tabulate(files, headers=columnes, tablefmt="fancy_grid"))
    else:
        print("⚠️ (Sense dades a aquesta taula)")

cursor.close()
conn.close()

print("\n✅ Finalitzat correctament.\n")
