from app import app, db, User, bcrypt, Comunidad, Factura, Treballador, Pagador, Calendari
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import time

def create_admin_user():
    with app.app_context():
        if User.query.filter_by(username='admin').first():
            print("El usuario admin ya existe.")
            return
        
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        user = User(
            username='admin',
            password=hashed_password,
            name='Jose Merchan',
            email='quality@maxilim.es',
            data_consent=True,
            consent_date=datetime.utcnow(),
            data_retention_days=365,
            role='admin'
        )
        db.session.add(user)
        try:
            db.session.commit()
            print("Usuario admin creado exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear usuario admin: {e}")

def create_employee():
    with app.app_context():
        if User.query.filter_by(username='empleado1').first():
            print("El usuario 'empleado1' ya existe.")
            return

        hashed_password = bcrypt.generate_password_hash('empleado123').decode('utf-8')
        new_employee = User(
            username='empleado1',
            name='Juan Pérez',
            email='juan.perez@empresa.com',
            password=hashed_password,
            role='employee',
            data_consent=True,
            consent_date=datetime.now(ZoneInfo("Europe/Madrid")),
            data_retention_days=365
        )

        db.session.add(new_employee)
        try:
            db.session.commit()
            print("Usuario empleado creado exitosamente.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear empleado: {e}")

def create_pagador():
    with app.app_context():
        if Pagador.query.filter_by(email='pagador@exemple.com').first():
            print("El pagador ja existeix.")
            return

        pagador = Pagador(
            nom_pagador='Pagador SL',
            telefon='934567890',
            email='pagador@exemple.com',
            direccio='Carrer Falsa 123',
            ciutat='Barcelona',
            codi_postal=8001
        )

        db.session.add(pagador)
        try:
            db.session.commit()
            print("Pagador creat amb èxit.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear pagador: {e}")

def create_comunitat():
    with app.app_context():
        if Comunidad.query.filter_by(cif='H99983').first():
            print("La comunitat 'H99983' ja existeix.")
            return

        pagador = Pagador.query.first()
        if not pagador:
            print("Cal crear un pagador abans.")
            return

        data_alta = datetime.strptime('12/04/2025', '%d/%m/%Y').date()

        nova_comu = Comunidad(
            nombre='Portal Rosello amb passeig de gràcia',
            cif='H99983',
            ciudad='Barcelona',
            codi_postal=8001,
            provincia='Barcelona',
            direccion='Rosello, 651',
            fecha_alta=data_alta,
            latitud=41.3925,
            longitud=2.1620,
            id_pagador=pagador.id_pagador
        )

        db.session.add(nova_comu)
        try:
            db.session.commit()
            print("Comunitat afegida exitosament.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear comunitat: {e}")

def create_factura():
    with app.app_context():
        comunitat = Comunidad.query.first()
        if not comunitat:
            print("Cal crear una comunitat abans.")
            return

        factura = Factura(
            id_comunitat=comunitat.id,
            tipus_feina='Limpieza mensual',
            document_de_pago='transferencia bancaria',
            regimen_impuestos='IVA 21%'
        )

        db.session.add(factura)
        try:
            db.session.commit()
            print("Factura creada amb èxit.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear factura: {e}")

def create_treballador():
    with app.app_context():
        usuari = User.query.filter_by(role='employee').first()
        if not usuari:
            print("Cal un usuari amb rol employee abans.")
            return

        treballador = Treballador(
            id_usuari=usuari.id,
            departament='comunitats',
            adreca='Carrer València 200',
            ciutat='Barcelona',
            codi_postal=8002,
            sexe='m',
            nacionalitat='Espanyola',
            edat=35,
            carnet_conduir='si',
            vehicle_propi='no'
        )

        db.session.add(treballador)
        try:
            db.session.commit()
            print("Treballador creat amb èxit.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear treballador: {e}")


def create_calendari():
    with app.app_context():
        treballador = Treballador.query.first()
        comunitat = Comunidad.query.first()

        if not treballador:
            print("Cal crear un treballador abans.")
            return
        if not comunitat:
            print("Cal crear una comunitat abans.")
            return

        # Exemple: assignem neteja dilluns i dimecres de 9 a 12h
        dies = ['Dll', 'Dx']
        hora_inici = time(9, 0)
        hora_fi = time(12, 0)

        for dia in dies:
            exists = Calendari.query.filter_by(
                treballador_id=treballador.id_treballador,
                dia_setmana=dia,
                comunitat_id=comunitat.id
            ).first()
            if exists:
                print(f"Ja existeix un registre per {dia}")
                continue

            nou_registre = Calendari(
                treballador_id=treballador.id_treballador,
                dia_setmana=dia,
                comunitat_id=comunitat.id,
                hora_inici=hora_inici,
                hora_fi=hora_fi
            )
            db.session.add(nou_registre)

        try:
            db.session.commit()
            print("Entrades de calendari creades amb èxit.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear entrades de calendari: {e}")



if __name__ == '__main__':
    create_admin_user()
    create_employee()
    create_pagador()
    create_comunitat()
    create_factura()
    create_treballador()
    create_calendari()