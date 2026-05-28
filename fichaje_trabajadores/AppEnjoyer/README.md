- [Tutorial d'ús de l'aplicació](#tutorial-dús-de-laplicació)
  - [Accés a l'aplicació](#accés-a-laplicació)
  - [Per a treballadors](#per-a-treballadors)
    - [Fitxar entrada i sortida](#fitxar-entrada-i-sortida)
    - [Gestionar pauses](#gestionar-pauses)
    - [Sol·licitar absències i teletreball](#sollicitar-absències-i-teletreball)
    - [Registrar incidències](#registrar-incidències)
    - [Fitxatge manual (si has oblidat fitxar)](#fitxatge-manual-si-has-oblidat-fitxar)
    - [Generar el teu informe en PDF](#generar-el-teu-informe-en-pdf)
    - [Perfil d'usuari](#perfil-dusuari)
  - [Per a administradors](#per-a-administradors)
    - [Tauler d'administració](#tauler-dadministració)
    - [Gestió de treballadors i usuaris](#gestió-de-treballadors-i-usuaris)
    - [Aprovar o denegar sol·licituds d'absència](#aprovar-o-denegar-sollicituds-dabsència)
    - [Calendari laboral](#calendari-laboral)
    - [Comunitats, pagadors i factures](#comunitats-pagadors-i-factures)
- [Employee Time Tracker](#employee-time-tracker)
  - [Características](#características)
  - [Tecnologías](#tecnologías)
  - [Instalación](#instalación)
  - [Instal·lació en servidor apache](#installació-en-servidor-apache)
  - [Licencia](#licencia)
  - [Manual de Git](#manual-de-git)
    - [Instruccions bàsiques Git (sino joaquim s'enfada)](#instruccions-bàsiques-git-sino-joaquim-senfada)
    - [Com crear una branca nova amb diferent informació](#com-crear-una-branca-nova-amb-diferent-informació)
    - [Esquema de branques per maxilim i organitzar el codi](#esquema-de-branques-per-maxilim-i-organitzar-el-codi)
  - [Crear base de dades i usuari mysql](#crear-base-de-dades-i-usuari-mysql)
  - [Gestió de la Base de Dades (Migracions)](#gestió-de-la-base-de-dades-migracions)
- [Desenvolupament de la app](#desenvolupament-de-la-app)
---

# Tutorial d'ús de l'aplicació

Aquest tutorial explica com fer servir l'aplicació **Employee Time Tracker** pas a pas. Està pensat per a qualsevol persona, sense necessitat de conèixer programació.

L'aplicació és una eina web de **control de presència i gestió laboral**. Permet als treballadors fitxar l'entrada i la sortida, gestionar pauses, sol·licitar absències i registrar incidències. Els administradors poden supervisar l'activitat de tot l'equip i gestionar les sol·licituds.

---

## Accés a l'aplicació

1. Obre el navegador web (Chrome, Firefox, Safari, etc.).
2. Entra a l'adreça web que t'hagi facilitat la teva empresa (exemple: `https://maxilim.nescolam.com`).
3. Apareixerà la pàgina d'**inici de sessió**. Introdueix el teu nom d'usuari i la teva contrasenya i clica **"Entrar"**.
4. Si has oblidat la contrasenya, fes clic a **"He oblidat la contrasenya"** i segueix les instruccions que rebràs per correu electrònic.

> **Nota:** Els comptes d'usuari els crea l'administrador de la teva empresa. No és possible registrar-se sol.

---

## Per a treballadors

### Fitxar entrada i sortida

Un cop has iniciat sessió, veuràs la pantalla principal amb el teu **estat actual**.

- Per **registrar l'entrada**: clica el botó verd **"Registrar Entrada"**. L'aplicació demanarà permís per accedir a la teva ubicació (GPS) i enregistrarà l'hora i la posició automàticament.
- Per **registrar la sortida**: quan acabis la jornada, clica el botó vermell **"Registrar Sortida"**. Igual que a l'entrada, es guardarà l'hora i la ubicació.
- A la part inferior de la pantalla podràs veure l'**historial de registres** de dies anteriors, amb hora d'entrada, sortida, durada i ubicació.

> Si han passat més de 5 minuts des que has entrat a l'aplicació i encara no has fitxat, apareixerà un recordatori automàtic perquè no t'oblidis.

### Gestionar pauses

Si durant la jornada fas una pausa (per dinar, descansar, etc.):

- Clica **"Començar Pausa"** (botó groc) quan t'aturis.
- Clica **"Acabar Pausa"** (botó verd) quan reprenguis la feina.
- Pots fer tantes pauses com necessitis. L'historial de pauses del dia apareixerà a la pantalla principal amb l'hora d'inici, fi i durada de cada pausa.

### Sol·licitar absències i teletreball

Pots demanar dies d'absència (vacances, baixa, assumptes personals) o dies de teletreball directament des de la pantalla principal.

1. A la secció **"Les meves Sol·licituds d'Absència"**, veuràs totes les teves sol·licituds actives i el seu estat (pendent o aprovada).
2. Per fer una nova sol·licitud, accedeix al **Calendari Laboral** (botó blau "Calendari Laboral") i selecciona els dies que vols sol·licitar.
3. Tria el tipus: **Vacances**, **Baixa mèdica**, **Assumptes personals** o **Teletreball**.
4. Pots adjuntar un justificant si cal (per exemple, un justificant mèdic).
5. La sol·licitud queda en estat **"Pendent"** fins que l'administrador l'aprovi o la denegui.
6. Si vols **cancel·lar** una sol·licitud pendent, clica el botó **"Cancel·lar"** al costat de la sol·licitud.

### Registrar incidències

Si durant la jornada passes per alguna situació especial (retard, problema tècnic, incidència laboral, etc.), pots deixar-ne constància:

1. Clica el botó vermell **"Registrar Incidència"** (disponible mentre tens una sessió de treball activa).
2. Selecciona la **categoria** (Retard, Problema tècnic, Incidència laboral, Altres).
3. Escriu una breu **descripció** del que ha passat.
4. Confirma l'hora i clica **"Envia"**. L'aplicació guardarà la ubicació automàticament.
5. Les incidències del dia apareixeran a la part inferior de la pantalla principal.

### Fitxatge manual (si has oblidat fitxar)

Si has oblidat registrar l'entrada (per exemple, perquè no tenies el mòbil a mà), pots introduir-la manualment:

1. Clica el botó **"Has oblidat registrar la teva entrada?"**.
2. S'obrirà un formulari on pots indicar la **data**, l'**hora d'entrada**, l'**hora de sortida** i les **hores de pausa** totals.
3. Clica **"Crear Registre"** per desar-ho.

> Tingues en compte que els registres manuals queden marcats com a tals i l'administrador pot veure'ls.

### Generar el teu informe en PDF

Pots descarregar un informe amb el teu historial de fitxatges:

1. Clica el botó blau **"Generar Informe"** a la pantalla principal.
2. L'aplicació generarà automàticament un fitxer **PDF** amb tots els teus registres horaris.
3. Guarda el fitxer al teu dispositiu per tenir-ne una còpia.

### Perfil d'usuari

Pots consultar les teves dades personals (nom, correu, telèfon, departament, adreça, etc.) accedint al teu **perfil d'usuari** des del menú de navegació superior.

---

## Per a administradors

Els administradors disposen de funcionalitats addicionals per gestionar l'empresa i els treballadors.

### Tauler d'administració

El **tauler d'administració** mostra un resum de l'activitat de tots els treballadors:

- Pots veure quins treballadors estan **treballant ara** (verd), en **pausa** (groc) o **inactius** (vermell).
- Fent clic sobre el nom d'un treballador accedeixes a la seva **fitxa detallada**, on pots veure les seves dades personals, l'historial complet de fitxatges i pauses, les sol·licituds d'absència i les incidències registrades.

### Gestió de treballadors i usuaris

Des de la pantalla principal (menú lateral dret), els administradors poden:

- **Veure la llista de treballadors** i consultar-ne les dades.
- **Crear nous treballadors** (amb dades com departament, adreça, nacionalitat, carnet de conduir, etc.).
- **Veure la llista d'usuaris** (comptes d'accés a l'aplicació).
- **Afegir nous usuaris** (empleats amb accés a l'app).
- **Afegir nous administradors** (amb permisos de gestió).

### Aprovar o denegar sol·licituds d'absència

Quan un treballador fa una sol·licitud d'absència o teletreball, apareix a la pantalla de **"Sol·licituds Pendents"**:

1. Accedeix a **"Sol·licituds d'Absència"** des del menú.
2. Veuràs una taula amb totes les sol·licituds pendents: treballador, empresa, tipus (Vacances, Baixa, Assumptes, Teletreball), dates, dies i justificant (si n'hi ha).
3. Clica **✅ Aprovar** per concedir la sol·licitud, o **❌ Denegar** per rebutjar-la.
4. La fila desapareixerà de la llista i el treballador veurà l'estat actualitzat de la seva sol·licitud.

### Calendari laboral

El **Calendari Laboral** permet visualitzar de forma gràfica les absències i esdeveniments de tots els treballadors. Des d'aquí, l'administrador també pot afegir dies festius o marcar events especials.

### Comunitats, pagadors i factures

L'apartat d'**Opcions Avançades** (menú lateral) inclou funcionalitats addicionals orientades a la gestió administrativa:

- **Comunitats**: gestió de les comunitats de propietaris o unitats de treball associades a l'empresa.
- **Pagadors**: gestió de les persones o entitats responsables de pagaments.
- **Factures**: creació i llistat de factures associades a l'activitat de l'empresa.

---

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
- Flask-Migrate
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
FLASK_APP=run.py
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
7. Instalar les bases de dades per la app, activant primer l'entorn virtual usant `python source env/bin/activate` (o similar) i després usant `python init_db.py`
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

## Manual de Git

### Instruccions bàsiques Git (sino joaquim s'enfada)

Instruccions de lectura:

1. `git status -sb`  Mostra l'estat actual del repositori en el commit on estem ara i les canvis fets que falta commitejar(el HEAD)
2. `git log` o `git log --graph --pretty=format:\"%C(auto)%h %C(green)%as %C(auto)%d %C(auto)% s\" --date=relative --branches --decorate` (copieu els alies del repository .gitconfig al vostre home, de [.gitconfig joaquim](https://github.com/joaquimbrugues/dotfiles) ) De fet copiar tot aixo al .gitconfig:
```
    [alias]
	s = status -sb
	c = commit
	a = add
	l = log --graph --pretty=format:\"%C(auto)%h %C(green)%as %C(auto)%d %C(auto)%s\" --date=relative --branches --decorate

    [pull]
        ff = only
    [fetch]
        prune = true

```
3. `git show 66yhhd` on 66yhhd és el nom del commit o de la branca, mostra tota la informació del commit seleccionat o l'últim commit de la branca o un tag.
4. `git remote -v` llista tots els servidors que estem seguint
5. `git branch -a` llista totes les branques locals
6. `git fetch --prune` serveix per netejar les referències de branques remotes esborrades


Instruccions de escriptura:

5. `git pull 'remote' 'branch'` descarrega els canvis del remote que demanis, si no poses res, fa el pull del servidor i branca remots que hi hagi a `git status`.
6. `git add .` afegeix tots els canvis 
7.  `commit` cada commit és un tros de la tija, amb la data, el missatge i els canvis realitzats, autor.
8.  `git commit` Abans de cometre hem de mirar en quina branca estem! El commit escriu els canvis en el registre de git, i desplaça la branca HEAD local, al commit fet.
9.  `git push 'remote' 'branch'` envia els canvis al remote que demanis, si no poses res, fa el push del servidor i branca remots que hi hagi a `git status`. Compte amb aquesta comanda!
10. `git checkout -b branch` crea una branca nova en el commit on estiguis (on està el HEAD).
11.  `git checkout -b branch 'commit'` crea una branca nova en el commit 'commit'.
12.  `git checkout -b branch 'remote'/'brancha remota'` crea una branca nova en el commit corresponent, i que segueix per fer pull i push a la branca remota 'remote'/'brancha remota'
13. `git checkout 'branch'` et mous a la branca 'branch'. 
14. `git branch -d 'branch'` eliminem la branca 'branch'
   

Instruccions per fer un commit ben fet

1. `git diff` mostra les diferències entre el que no està afegit, i l'últim commit
2. `git add fitxer1 fitxer2 ....` afegeix per fer commit, tots els fitxers amb els canvis que vulguis afegir
3. O també podem fer `git add -u` no afegeix fitxers nous encara que no estiguin afegits mai, només afageix canvis que ja estiguessin en algun commit.
4. `git reset` desfà el `git add`
5. `git commit -m 'missatge sobre els canvis'` grava els canvis en un commit local. Sinó també podem fer `git commit` i escriure en el editor que surt un títol del commit (la primera línia de la pàgina) i una descripció (les següents línies del fitxer)
   
Instruccions avançades

1. `git merge 'branch2'` fusiona la branca 'branch2' a la branca actual.
2. Si hi ha un conflicte, escriure `git status`
3. Els conflictes estan marcats amb uns: 
```
<<<<< HEAD
# canvis a head local
=======
# canvis de la branca que estás fusionant que entren en conflicte
>>>>> branch2
```
4. Per arreglar un conflicte s'ha d'editar el fitxer a mà i seleccionar una de les dues versions o un mix.


### Com crear una branca nova amb diferent informació

Principi 1: Volem tenir el mínim de branques possibles i esborrarles tan aviat com sigui possible.
Principi 2: Els merges sempre van en una direcció

Dia a dia de treballar en una nova funcionalitat (pagadors)
1. Penso en quina feina vull treballar
2. Em col·loco en la branca on vull treballar `pagadors`
3. Fer pull de la branca remota `pagadors`.
4. Posar-me a la branca `dev` i fer pull
5. tornar a la branca `pagadors`
6. Fer merge de la branca `dev` en la branca `pagadors` per tenir tot actualitzat a la branca pagadors usant `git merge dev` per escriure els canvis de "dev" a "pagadors"
7. Treballem en la branca `pagadors` i mirem que estem a la branca que toca fent `git branch` i si estem a `pagadors` fem commits.
8. Fem un pull per seguretat si hi ha coses noves, a `pagadors`
9. Si tot va bé, fem `push`.

### Esquema de branques per maxilim i organitzar el codi

Tindrem dues branques principals. `estable` i `dev`
1. `estable` és la branca de producció, no es canvia mai, i només es fa merge cap a ella desde `dev`. I només es fa el merge després de veure que `dev` funciona correctament.
2. De la branca `dev` es faran merges d'altres branquetes com perexemple `pagadors` `crear_factura` `geolocalitzacio` incorporant petits canvis a dev. 
3. També es poden fer canvis directament a `dev`.
4. Un cop els canvis de les petites branques s'han incorporat a `dev` el joaquim diu que s'esborra la branca :(. (i els maniqueus diuen que té raó. :/)
```
    *   | 
    | \ | 
    |  \*
    |   *   
    |   | \ 
    |   |  \
    |   |   *
    |   *   *
    *   |   *
    | \ * / |
    |  \|/  |
    *   *   *
    | \ | / |
    |  \|/ gelocalització
    |   *
    |   dev
    |
  estable
```

## Crear base de dades i usuari mysql

    Create database "whatever"
    CREATE USER 'user'@'localhost' IDENTIFIED BY 'passi';
    GRANT ALL PRIVILEGES ON meva_base.* TO 'nou_usuari'@'localhost';

## Gestió de la Base de Dades (Migracions)

Per gestionar els canvis en l'estructura de la base de dades (afegir columnes, crear taules, etc.) sense perdre les dades existents, fem servir **Flask-Migrate**.

### 1. Inicialitzar el repositori de migracions
Només cal fer-ho una vegada al principi del projecte:
```bash
flask db init
```

### 2. Generar una migració
Cada vegada que facis un canvi als models (`app/models.py`), has de generar un fitxer de migració:
```bash
flask db migrate -m "Descripció dels canvis (ex: afegir columna telèfon)"
```

### 3. Aplicar els canvis a la base de dades
Perquè els canvis siguin efectius a la base de dades real:
```bash
flask db upgrade
```

### 4. Desfer canvis (opcional)
Si t'has equivocat i vols tornar enrere a la versió anterior:
```bash
flask db downgrade
```


# Desenvolupament de la app


Idea del sistema d'arxius en arbre:

    AppEnjoyer/
    │
    ├── app/
    │   ├── __init__.py        ← crea app + config + db + login
    │   ├── models.py          ← totes les taules SQLAlchemy
    │   ├── routes/
    │   │   ├── auth.py
    │   │   ├── treballadors.py
    │   │   ├── comunitats.py
    │   │   ├── calendari.py
    │   │   ├── factures.py
    │   │   └── api.py
    │   │
    │   ├── services/
    │   │   ├── pdf_service.py
    │   │   ├── email_service.py
    │   │   └── user_service.py
    │   │
    │   ├── utils.py
    │   └── templates/
    │       ├── base.html
    │       ├── auth/
    │       │   ├── login.html
    │       │   ├── create_user.html
    │       │   └── register_first_admin.html
    │       │
    │       ├── empresa/
    │       │   ├── create_empresa.html
    │       │   ├── generate_empresa_link.html
    │       │   └── create_admin.html
    │       │
    │       ├── treballadors/
    │       │   ├── create_treballador.html
    │       │   └── llistat_treballadors.html
    │       │
    │       ├── comunitats/
    │       │   ├── create_comunitat.html
    │       │   └── llistat_comunitats.html
    │       │
    │       ├── factures/
    │       │   ├── create_factura.html
    │       │   └── llistat_factures.html
    │       │
    │       ├── pagadors/
    │       ├── calendari/
    │       └── legal/
    │           ├── privacy_policy.html
    │           └── aviso_legal.html
    │
    ├── create_dades.py
    ├── init_db.py
    ├── run.py
    └── .env
