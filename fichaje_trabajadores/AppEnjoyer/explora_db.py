import pymysql
import os
from dotenv import load_dotenv

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
print("Taules disponibles:")
for taula in taules:
    print(f"\n- {taula}")
    cursor.execute(f"DESCRIBE {taula};")
    columnes = [c[0] for c in cursor.fetchall()]
    print("  Columnes:", columnes)

    cursor.execute(f"SELECT * FROM {taula} LIMIT 5;")
    files = cursor.fetchall()
    for fila in files:
        print("  ", fila)

cursor.close()
conn.close()
