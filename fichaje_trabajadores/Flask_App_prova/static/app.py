from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia esto según tu configuración de MySQL
app.config['MYSQL_PASSWORD'] = 'Dinamarca24+'  # Tu contraseña de MySQL
app.config['MYSQL_DB'] = 'database'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    nom = request.form['nom']
    correu = request.form['correu']
    contrasenya = request.form['contrasenya']
    departament = request.form['departament']
    tipus_permis = request.form['tipus_permis']

    hashed_password = generate_password_hash(contrasenya, method='sha256')

    cursor = mysql.connection.cursor()

    try:
        # Inserta en treballadors
        cursor.execute('''
            INSERT INTO treballadors (nom_i_cognom, correu, contrasenya, departament, created_at) 
            VALUES (%s, %s, %s, %s, NOW())
        ''', (nom, correu, hashed_password, departament))
        
        # Opcional: guardar también en usuaris si deseas (aunque no hay campo que los enlace)
        cursor.execute('''
            INSERT INTO usuaris (tipus_usuari, tipus_permis, created_at) 
            VALUES (%s, %s, NOW())
        ''', ('treballador', tipus_permis))

        mysql.connection.commit()
        cursor.close()

        flash('Treballador registrat correctament!', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return f'Error en registrar el treballador: {e}'
