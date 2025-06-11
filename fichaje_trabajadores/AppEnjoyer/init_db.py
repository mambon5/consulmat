from app import db, app
from create_dades import (
    create_admin_user, 
    create_employee, 
    create_comunitat,
    create_pagador,
    create_factura,
    create_treballador
)

def init_database():
    with app.app_context():
        print("Iniciando configuración de la base de datos...")
        try:
            # Crear todas las tablas si no existen
            db.create_all()
            print("Tablas creadas correctamente.")
            
            # Crear registros iniciales
            create_admin_user()
            create_employee()
            create_pagador()
            create_comunitat()
            create_factura()
            create_treballador()
            
            print("Inicialización de la base de datos completada.")
        except Exception as e:
            print(f"Error durante la inicialización de la base de datos: {e}")
            raise e

if __name__ == '__main__':
    init_database()
