# config.py
import os

DB_USER = 'administra'
DB_PASSWORD = 'anamas??99'
DB_HOST = 'localhost'
DB_NAME = 'anamas'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
