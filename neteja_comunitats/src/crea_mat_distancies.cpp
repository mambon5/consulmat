
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

vector<vector<int>> llegir_csv(const string &nom_fitxer) {
    vector<vector<int>> matriu(N, vector<int>(N, INF));
    cout << "Llegint el fitxer: " << nom_fitxer << " ... " << endl;
    ifstream fitxer(nom_fitxer);
    if (!fitxer) {
        cerr << "No s'ha pogut obrir el fitxer: " << nom_fitxer << endl;
        exit(1);
    }
    
    string linia;
    while (getline(fitxer, linia)) {
        stringstream ss(linia);
        int origen, desti, temps;
        char coma;
        // cout << "llegint linia: " << linia << endl;
        if (ss >> origen >> coma >> desti >> coma >> temps) {
            // cout << "llegint ... " << origen << " " << desti << " " << temps << endl;
            // condicio de simetria: ( en ppi ja s'ha llegit el valor origen  < desti)
            if(origen > desti) matriu[origen][desti] = matriu[desti][origen];
            else matriu[origen][desti] = temps;
        }
    }
    fitxer.close();
    cout << "Lectura acabada" << endl;
    return matriu;
}

void guardar_csv(const string &nom_fitxer, const vector<vector<int>> &matriu) {
    ofstream fitxer(nom_fitxer);
    if (!fitxer) {
        cerr << "No s'ha pogut crear el fitxer: " << nom_fitxer << endl;
        exit(1);
    }
    
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (matriu[i][j] == INF)
                fitxer << "INF";
            else
                fitxer << matriu[i][j];
            if (j < N - 1) fitxer << ",";
        }
        fitxer << "\n";
    }
    fitxer.close();
}

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