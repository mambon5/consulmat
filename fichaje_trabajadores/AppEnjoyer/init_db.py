from app import db, app
from create_dades import (
    create_empresa1,
    create_empresa2,
    create_admin_user1, 
    create_admin_user2,
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
            empresa = create_empresa1()
            if empresa:
                create_admin_user1(empresa.id)
            else:
                print("No se pudo crear la empresa. No se crearán usuarios ni trabajadores.")

            # Crear registros iniciales
            empresa = create_empresa2()
            if empresa:
                create_admin_user2(empresa.id)
                create_treballador(empresa.id)
            else:
                print("No se pudo crear la empresa. No se crearán usuarios ni trabajadores.")
            create_pagador()
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
