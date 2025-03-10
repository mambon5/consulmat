# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 00:59:12 2025

@author: ruthv
"""


from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Conectar con la base de datos
def init_db():
    conn = sqlite3.connect('trabajadores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fichajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            hora_entrada TEXT,
            hora_salida TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página principal
@app.route('/')
def index():
    conn = sqlite3.connect('trabajadores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fichajes')
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

# Registro de entrada
@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        nombre = request.form['nombre']
        hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect('trabajadores.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO fichajes (nombre, hora_entrada) VALUES (?, ?)', (nombre, hora_entrada))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('registro.html', tipo="Entrada")

# Registro de salida
@app.route('/salida/<int:id>', methods=['GET', 'POST'])
def salida(id):
    if request.method == 'POST':
        hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect('trabajadores.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE fichajes SET hora_salida = ? WHERE id = ?', (hora_salida, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('registro.html', tipo="Salida", id=id)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
