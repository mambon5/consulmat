import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/consulmat/fichaje_trabajadores/AppEnjoyer')

from app import app as application
