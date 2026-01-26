# utils.py
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from datetime import datetime

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def utility_processor():
    return {'now': datetime.now()}


