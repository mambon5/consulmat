# Projecte organitzacio neteja QMAxilim

# Organització del codi

Bones, hi ha diferents arxius i projeces en aquest repositori:

- El projecte inicial de netejar parquings es troba a la carpeta "neteja pàrquings". Allà dins hi ha la carpeta `scip` que conté el fitxer `creador_fitxer_lp_optimitzacio_gral.cpp` el qual crea la funcio a optimitzar, i les restriccions, i les guarda al fitxer `problem_big.lp`. Per executar el model d'otpimització es crida al programa `scip` i se li passa aquest fitxer `.lp`. L'output està guardat a `problem_lp.out`.
- La carpeta `neteja_comunitats` amb tota la merda que està fent el romà per organitzar el tema neteja de comunitats
- La carpeta `TSP Clean` amb tot el que està fent la Root-Rut respecte la neteja de comuntiats
- La carpeta `Fichaje treballadores` amb tot el que estem fent (la rut) respecte fitxatxe de treballadors.