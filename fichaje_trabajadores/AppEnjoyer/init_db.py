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
                create_treballador(empresa.id) # treballador per defecte
                create_treballador(             # tres treballadors addicionals
                    empresa.id,
                    username="empleado2",
                    password="empleado123",
                    name="Carlos Martínez",
                    email="carlos.martinez@empresa.com",
                    phone="611234567",
                    departament="manteniment",
                    adreca="Carrer Aragó 145",
                    ciutat="Barcelona",
                    codi_postal=8007,
                    sexe="m",
                    nacionalitat="Espanyola",
                    edat=42,
                    carnet_conduir="si",
                    vehicle_propi="si",
                    role="employee"
                )

                create_treballador(
                    empresa.id,
                    username="empleado3",
                    password="empleado123",
                    name="Laura Gómez",
                    email="laura.gomez@empresa.com",
                    phone="622345678",
                    departament="administracio",
                    adreca="Carrer Provença 310",
                    ciutat="Barcelona",
                    codi_postal=8037,
                    sexe="f",
                    nacionalitat="Espanyola",
                    edat=29,
                    carnet_conduir="no",
                    vehicle_propi="no",
                    role="employee"
                )

                create_treballador(
                    empresa.id,
                    username="empleado4",
                    password="empleado123",
                    name="Ahmed Benali",
                    email="ahmed.benali@empresa.com",
                    phone="633456789",
                    departament="comunitats",
                    adreca="Carrer Marina 220",
                    ciutat="Barcelona",
                    codi_postal=8013,
                    sexe="m",
                    nacionalitat="Marroquina",
                    edat=37,
                    carnet_conduir="si",
                    vehicle_propi="no",
                    role="employee"
                )
 


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
