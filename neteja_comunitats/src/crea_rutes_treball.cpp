
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <limits>

#include "textProcess.h"
#include <vector>
// compilar usant
// g++ dates.cpp textProcess.cpp crea_mat_distancies.cpp -o crea_matD -lcurl

using namespace std;

const int N = 355; // Nombre de comunitats
const int INF = numeric_limits<int>::max();

// crea un programa en cpp que donat aquestes dues columnes, de diferents tipus de neteja ques'han de fer cada setmana a cada comunitat

// E's and V's.txt
// 1	0
// 1	1
// 1	0
// 1	1
// 1	4
// 1	0
// 1	0
// 1	0
// 1	0
// 1	0
// 1	0
// 0	0
// 1	1
// 1	0
// ...
// Cada E tarda 1.5h de treball i cada V uns 30min

// la matriu de distàncies a peu entre cada comunitat, MDistPeu.csv
// 0,13,69,480,9,7,7
// 13,0,78,420,9,17,17
// 69,78,0,480,78,64,64
// 480,420,480,0,480,480,480
// 9,9,78,480,0,16,16
// 7,17,64,480,16,0,1
// 7,17,64,480,16,1,0

// (per a 7 comunitats) que dona els temps de la comunitat i (fila) a la j(columna) en minuts

// assigni fins a 40 treballadors de la següent manera.
// EL primer tria una comunitat que faci motls dies a la setmana. la regla es la següent per decidir quins dies de la setmana es neteja:



int main() {
    // fitxer d'accés global
    string currentDate = getCurrentDate();
    string data = "2025-03-16"; // borrar aquesta linia per seguretat.
    //input
    string inDistCotxe="../input/DistCotxe_"+data+".csv";
    string inDistMetro="../input/DistMetro_"+data+".csv";
    string inDistPeu="../input/DistPeu_"+data+".csv";
    string inDistBici="../input/DistBici_"+data+".csv";
    // output
    string DistCotxe="../output/MDistCotxe_"+currentDate+".csv";
    string DistMetro="../output/MDistMetro_"+currentDate+".csv";
    string DistPeu="../output/MDistPeu_"+currentDate+".csv";
    string DistBici="../output/MDistBici_"+currentDate+".csv";
    
    vector<vector<int>> matriu = llegir_csv(inDistCotxe);
    guardar_csv(DistCotxe, matriu);
    matriu = llegir_csv(inDistMetro);
    guardar_csv(DistMetro, matriu);
    matriu = llegir_csv(inDistPeu);
    guardar_csv(DistPeu, matriu);
    matriu = llegir_csv(inDistBici);
    guardar_csv(DistBici, matriu);

    
    cout << "Matrius guardades, exemple: " << DistPeu << endl;
    return 0;
}