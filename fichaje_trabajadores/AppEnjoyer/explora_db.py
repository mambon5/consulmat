import sqlite3

# Connexió al fitxer SQLite
conn = sqlite3.connect('instance/employee_time.db')
cursor = conn.cursor()

# Mostrar totes les taules
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
taules = cursor.fetchall()
print("Taules disponibles:")
for t in taules:
    print("-", t[0])

# Exemple: Mostrar les primeres files d'una taula concreta
taula = taules[1][0]  # Agafa la primera taula (canvia-ho si vols)
print(f"\nMostrant dades de la taula '{taula}':")
cursor.execute(f"SELECT * FROM {taula} LIMIT 5;")
files = cursor.fetchall()
for fila in files:
    print(fila)

# Tanca la connexió
conn.close()
