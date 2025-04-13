# app.py
from flask import Flask, jsonify, request, render_template
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Treballador

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# Crear la base de dades si no existeix
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/treballadors', methods=['GET', 'POST'])
def get_treballadors():
    treballadors = Treballador.query.all()
    return jsonify([t.as_dict() for t in treballadors])

def crear_treballador():
    data = request.json
    nou = Treballador(
        nom_i_cognom=data['nom_i_cognom'],
        departament=data['departament'],
        correu=data['correu'],
        contrasenya=data['contrasenya'],
        id_comunitat=data.get('id_comunitat')
    )
    db.session.add(nou)
    db.session.commit()
    return jsonify({'missatge': 'Treballador afegit!'}), 201

def treballadors():
    if request.method == 'GET':
        # Obtenir i retornar la llista de treballadors
        return get_treballadors()
    elif request.method == 'POST':
        # Crear un nou treballador
        return crear_treballador()

if __name__ == '__main__':
    app.run(debug=True)
