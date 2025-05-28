# Projecte organitzacio neteja QMAxilim

## Organització del codi

Bones, hi ha diferents arxius i projeces en aquest repositori:

- El projecte inicial de netejar parquings es troba a la carpeta "neteja pàrquings". Allà dins hi ha la carpeta `scip` que conté el fitxer `creador_fitxer_lp_optimitzacio_gral.cpp` el qual crea la funcio a optimitzar, i les restriccions, i les guarda al fitxer `problem_big.lp`. Per executar el model d'otpimització es crida al programa `scip` i se li passa aquest fitxer `.lp`. L'output està guardat a `problem_lp.out`.
- La carpeta `neteja_comunitats` amb tota la merda que està fent el romà per organitzar el tema neteja de comunitats
- La carpeta `TSP Clean` amb tot el que està fent la Root-Rut respecte la neteja de comuntiats
- La carpeta `Fichaje treballadores` amb tot el que estem fent (la rut) respecte fitxatxe de treballadors.

## Fitxatge treballadors: INICIAR APP FLASK
### Primer cop activar App
cd C:\Users\ruthv\Documents\PROJECTES\Maximiliam_APP\consulmat\fichaje_trabajadores\AppEnjoyer\

pip install -r C:\Users\ruthv\Documents\PROJECTES\Maximiliam_APP\consulmat\fichaje_trabajadores\AppEnjoyer\requirements.txt

python init_db.py (això només el primer cop: inicialitza base de dades i crea usuari admin ; contra: admin123 i crea usuari_treballador empleado1; contra: empleado123)

flask --app app.py run

### Quan ja s'ha clonat la App i s'ha inicialitzat la db: 
Accedir ubi on están els arxius App, activar environment de conda i Iniciar Flask

cd "C:\Users\ruthv\Documents\PROJECTES\Maximiliam_APP\consulmat\fichaje_trabajadores\AppEnjoyer"

conda activate env_app_Enjoyer

flask --app app.py run


## Neteja comunitats

## Neteja pàrquings

## TSP Clean
