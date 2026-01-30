import sys
import logging
from dotenv import load_dotenv  # ← AIXÒ ET FALTAVA

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/consulmat/fichaje_trabajadores/AppEnjoyer')

# Carregar .env
load_dotenv('/var/www/consulmat/fichaje_trabajadores/AppEnjoyer/.env')


from run import app as application
