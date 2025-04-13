# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Treballador(db.Model):
    __tablename__ = 'treballadors'
    id_treballador = db.Column(db.Integer, primary_key=True)
    nom_i_cognom = db.Column(db.String(255), nullable=False)
    departament = db.Column(db.String(255), nullable=False)
    correu = db.Column(db.String(255), nullable=False, unique=True)
    contrasenya = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id_treballador': self.id_treballador,
            'nom_i_cognom': self.nom_i_cognom,
            'departament': self.departament,
            'correu': self.correu,
            'created_at': self.created_at.isoformat()
        }