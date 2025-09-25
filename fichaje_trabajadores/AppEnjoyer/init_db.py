from app import db, app
from create_dades import (
    create_empresa,
    create_admin_user, 
    create_comunitat,
    create_pagador,
    create_factura,
    create_treballador,
    create_calendari
)

def init_database():
    with app.app_context():
        print("Iniciando configuración de la base de datos...")
        try:
            # Crear todas las tablas si no existen
            db.create_all()
            print("Tablas creadas correctamente.")
            
            # Crear registros iniciales
            empresa = create_empresa()
            if empresa:
                create_admin_user(empresa.id)
                create_treballador(empresa.id)
            else:
                print("No se pudo crear la empresa. No se crearán usuarios ni trabajadores.")
            create_pagador()
            create_comunitat()
            create_factura()
            create_calendari()
            
            print("Inicialización de la base de datos completada.")
        except Exception as e:
            print(f"Error durante la inicialización de la base de datos: {e}")
            raise e

if __name__ == '__main__':
    init_database()
