import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/consulmat/fichaje_trabajadores/AppEnjoyer')

# Carregar .env
load_dotenv('/var/www/consulmat/fichaje_trabajadores/AppEnjoyer/.env')

from app import app as application
