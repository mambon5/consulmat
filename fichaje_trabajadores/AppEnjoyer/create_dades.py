from app import app, db, User, bcrypt, Comunidad
from datetime import datetime
from zoneinfo import ZoneInfo



def create_admin_user():
    with app.app_context():
        # Verificar si el usuario admin ya existe
        if User.query.filter_by(username='admin').first():
            print("El usuario admin ya existe.")
            return
        
        # Crear usuario administrador
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
        # Verificar si el usuario ya existe
        if User.query.filter_by(username='empleado1').first():
            print("El usuario 'empleado1' ya existe.")
            return

        # Crear nuevo empleado
        hashed_password = bcrypt.generate_password_hash('empleado123').decode('utf-8')
        new_employee = User(
            username='empleado1',
            name='Juan Pérez',
            email='juan.perez@empresa.com',
            password=hashed_password,
            role='employee',
            data_consent=True,
            consent_date = datetime.now(ZoneInfo("Europe/Madrid"))
            data_retention_days=365
        )

        # Añadir y confirmar en la base de datos
        db.session.add(new_employee)
        try:
            db.session.commit()
            print("Usuario empleado creado exitosamente.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear empleado: {e}")

def create_comunitat():
    with app.app_context():
        # Verificar si el comunitat ya existe
        if Comunidad.query.filter_by(nif='H99983').first():
            print("La comunitat 'H99983' ya existe.")
            return

        # Convertim el string a un objecte datetime.date
        data_alta = datetime.strptime('12/04/2025', '%d/%m/%Y').date()

        # Crear nuevo comunitat
        nova_comu = Comunidad(
            nombre='Portal Rosello amb passeig de gràcia',
            nif='H99983',
            ciudad='Barcelona',
            provincia='Barcelona',
            direccion='Rosello, 651',
            fecha_alta=data_alta  # <-- ara és un date object
        )

        # Añadir y confirmar en la base de datos
        db.session.add(nova_comu)
        try:
            db.session.commit()
            print("Comunitat afegida exitosament.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear comunitat: {e}")

if __name__ == '__main__':
    create_admin_user()
    create_employee()
