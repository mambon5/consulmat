# create_dades.py

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from app.models import (
    User, Comunidad, Factura, Treballador, Pagador, Empresa, Calendari
)
from datetime import datetime, time

# Crear instància de Flask amb la factory
app = create_app()


# -----------------------------
# Funcions per crear dades
# -----------------------------

def create_empresa1():
    num_fisc = 'B1278'
    empresa = Empresa.query.filter_by(numero_fiscal=num_fisc).first()
    if empresa:
        print(f"La empresa amb número fiscal {num_fisc} ja existeix.")
        return empresa

    hashed_password = bcrypt.generate_password_hash('empresa123').decode('utf-8')
    empresa = Empresa(
        nom='Anamas digital',
        password=hashed_password,
        numero_fiscal=num_fisc,
        adreca='Carrer duoda 21, 08020, Barcelona',
        correu_gerent='anamasdigital@gmail.com',
        telefon_gerent='611648478'
    )
    db.session.add(empresa)
    try:
        db.session.commit()
        print(f"Empresa {empresa.nom} creada exitosament")
        return empresa
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear la empresa: {e}")
        return None


def create_empresa2():
    num_fisc = 'B12345678'
    empresa = Empresa.query.filter_by(numero_fiscal=num_fisc).first()
    if empresa:
        print(f"La empresa amb número fiscal {num_fisc} ja existeix.")
        return empresa

    hashed_password = bcrypt.generate_password_hash('empresa123').decode('utf-8')
    empresa = Empresa(
        nom='Quality Maxilim SL',
        password=hashed_password,
        numero_fiscal=num_fisc,
        adreca='Carrer de Joanot Martorell, 5, 08403 Granollers, Barcelona',
        correu_gerent='qmaxi@gmail.com',
        telefon_gerent='647112622'
    )
    db.session.add(empresa)
    try:
        db.session.commit()
        print(f"Empresa {empresa.nom} creada exitosament")
        return empresa
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear la empresa: {e}")
        return None


def create_user(username, password, name, email, role, empresa_id, phone=None):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"El usuario '{username}' ya existe.")
        return existing_user

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        username=username,
        password=hashed_password,
        name=name,
        email=email,
        phone=phone,
        data_consent=True,
        consent_date=datetime.utcnow(),
        data_retention_days=365,
        role=role,
        empresa_id=empresa_id
    )
    db.session.add(user)
    try:
        db.session.commit()
        print(f"Usuario {role} '{username}' creado exitosamente.")
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear usuario {role}: {e}")
        return None


# Creació d’administradors
def create_admin_user1(empresa_id):
    return create_user(
        username="admin",
        password="admin123",
        name="Ruth Masa",
        email="masaruth@anamas.es",
        role="admin",
        empresa_id=empresa_id,
        phone="611171"
    )

def create_admin_user2(empresa_id):
    return create_user(
        username="jose",
        password="admin123",
        name="Jose Merchan",
        email="quality@maxilim.es",
        role="admin",
        empresa_id=empresa_id,
        phone="600123456"
    )


# Creació d’empleats
def create_treballador(
    empresa_id, username="empleado1", password="empleado123",
    name="Juan Pérez", email="juan.perez@empresa.com", phone="600123456",
    departament='comunitats', adreca='Carrer València 200', ciutat='Barcelona',
    codi_postal=8002, sexe='m', nacionalitat='Espanyola', edat=35,
    carnet_conduir='si', vehicle_propi='no', role="employee"
):
    user = create_user(username, password, name, email, role, empresa_id, phone)
    if user:
        # Verificar si ja existeix la fitxa de treballador
        existing_treballador = Treballador.query.filter_by(id_usuari=user.id).first()
        if existing_treballador:
            print(f"La fitxa de treballador per '{username}' ja existeix.")
            return

        treballador = Treballador(
            id_usuari=user.id,
            empresa_id=empresa_id,
            departament=departament,
            adreca=adreca,
            ciutat=ciutat,
            codi_postal=codi_postal,
            sexe=sexe,
            nacionalitat=nacionalitat,
            edat=edat,
            carnet_conduir=carnet_conduir,
            vehicle_propi=vehicle_propi
        )
        db.session.add(treballador)
        try:
            db.session.commit()
            print(f"Treballador per usuari '{user.username}' creat correctament.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear treballador per usuari {user.username}: {e}")


def create_pagador():
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


def create_calendari():
    treballador = Treballador.query.first()
    comunitat = Comunidad.query.first()

    if not treballador or not comunitat:
        print("Cal crear primer un treballador i una comunitat.")
        return

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


# -----------------------------
# Execució principal
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        empresa1 = create_empresa1()
        if empresa1:
            create_admin_user1(empresa1.id)

        
        empresa2 = create_empresa2()
        if empresa2:
            create_admin_user2(empresa2.id)
        
        create_pagador()
        create_comunitat()
        create_factura()
        create_calendari()
