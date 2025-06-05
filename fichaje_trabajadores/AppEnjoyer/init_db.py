from app import db, app
from create_dades import create_admin_user,create_employee, create_comunitat

def init_database():
    with app.app_context():
        print("Iniciando configuración de la base de datos...")
        try:
            # Crear todas las tablas si no existen
            db.create_all()
            print("Tablas creadas correctamente.")
            
            # Crear usuario administrador inicial
            create_admin_user()

            # Crear usuario pobre inicial
            create_employee()

            # Create comunitat
            create_comunitat()
            
            print("Inicialización de la base de datos completada.")
        except Exception as e:
            print(f"Error durante la inicialización de la base de datos: {e}")
            raise e

if __name__ == '__main__':
    init_database()
