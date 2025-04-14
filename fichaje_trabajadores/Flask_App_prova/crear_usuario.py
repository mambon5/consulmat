from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configuración de MySQL (ajusta según tu setup)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'app_fitxatge'

mysql = MySQL(app)

with app.app_context():
    hashed_password = generate_password_hash('mi_contraseña123', method='sha256')
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO usuaris (correu, contrasenya, tipus_usuari, tipus_permis) VALUES (%s, %s, %s, %s)', 
                   ('admin@ejemplo.com', hashed_password, 'admin', 'alt'))
    mysql.connection.commit()
    cursor.close()
    print("✅ Usuario creado con éxito.")
