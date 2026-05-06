import sys
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Add the app directory to sys.path
sys.path.append('/var/www/consulmat/fichaje_trabajadores/AppEnjoyer')

load_dotenv()

def get_db_url():
    if os.environ.get('DATABASE_URL'):
        return os.environ.get('DATABASE_URL')
    
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'fichaje_db')
    
    if DB_PASSWORD:
        return f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        return f'mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(get_db_url())

def add_column(table, column, definition):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}"))
            conn.commit()
            print(f"Added column {column} to table {table}")
    except Exception as e:
        if "Duplicate column name" in str(e):
            print(f"Column {column} already exists in table {table}")
        else:
            print(f"Error adding column {column} to table {table}: {e}")

if __name__ == "__main__":
    add_column("time_record", "fitxatge_amb_retard", "BOOLEAN DEFAULT FALSE NOT NULL")
    add_column("eventos_laborales", "justificante_path", "VARCHAR(255) NULL")
