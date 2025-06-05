# Employee Time Tracker

Una aplicación web desarrollada con Flask para el seguimiento del tiempo de los empleados.

## Características

- Registro de entrada y salida de empleados
- Generación de informes de tiempo
- Panel de administración
- Gestión de usuarios
- Exportación de informes en PDF
- Políticas de privacidad y consentimiento de datos

## Tecnologías

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- ReportLab
- PostgreSQL (producción)
- SQLite (desarrollo)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/IaEnjoyer/employee-time-tracker.git
cd employee-time-tracker
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear un archivo `.env` con:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
```

5. Iniciar la aplicación:
```bash
flask run
```

## Instal·lació en servidor apache

1. Seguir els mateixos passos que en "Instalación"
2. Crear un virtual hosts que escolti al port :80 a `/etc/apache2/sites-available/` anomenat `subodmini.conf`. Posar allà la info necessària de server i la carpeta on està la aplicació, com exemple:
    ```
    <VirtualHost *:80>
        ServerName maxilim.nescolam.com

        DocumentRoot /var/www/consulmat/fichaje_trabajadores/AppEnjoyer

        <Directory /var/www/consulmat/fichaje_trabajadores/AppEnjoyer>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/maxilim_error.log
        CustomLog ${APACHE_LOG_DIR}/maxilim_access.log combined
    RewriteEngine on
    RewriteCond %{SERVER_NAME} =maxilim.nescolam.com [OR]
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>
    ```

3. Instalar WSGI per fer l'interacció entre apache i python i que corri l'aplicació per si sola en apache
    ```
        sudo apt update
        sudo apt install libapache2-mod-wsgi-py3
    ```
4. Fer correr el certbot de linux per instalar el certificat ssl i passar de http a https usant `sudo certbot`
5. Afegir les següents línies de codi al virtual host de port :443 que ha creat certbot:
    ```
    WSGIDaemonProcess maxilim python-home=/var/www/consulmat/fichaje_trabajadores/AppEnjoyer/envi python-path=/var/www/consulmat/fichaje_trabajadores/AppEnjoyer
    WSGIProcessGroup maxilim
    WSGIScriptAlias / /var/www/consulmat/fichaje_trabajadores/AppEnjoyer/config.wsgi
    WSGIPassAuthorization On
    ```
    just després d'on diu DocumentRoot.

6. Eliminar les bases de dades prèvies que pugui haver-hi, usant `sudo rm -r instances`.
7. Instalar les bases de dades per la app, activant primer l'entorn virtual i després usant `python init_db.py`
8. Donar permisos. Donar permisos al servei apache `www-data` perquè pugui escriure a la base de dades, usant les comandes:
    ```
    sudo chown -R usuari_qualsevol:www-data /var/www/consulmat/fichaje_trabajadores/AppEnjoyer
    sudo chmod -R 775 /var/www/consulmat/fichaje_trabajadores/AppEnjoyer
    ```

9.  Reiniciar el servidor apache per gravar els canvis:
    ```
        sudo systemctl restart apache2.service 
    ```
10. Anar a la pàgina web on s'ha comprat el domini, accedir a l'apartat de DNS, i afegir un Dynamic DNS A record amb el subdomini.domini.com i la direcció IP IPv4 del servidor on estigui hostejat els arxius i el servidor apache.


## Licencia

Este proyecto está bajo la licencia MIT.
