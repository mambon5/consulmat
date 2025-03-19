#include <iostream>
#include <vector>
#include <limits>
#include "src/textProcess.h"



// compile by the command: 
// g++  src/dates.cpp src/textProcess.cpp neteja_parquings_4_domicilis_heuristic.cpp -o heuristic

using namespace std;

void netejaParkings(vector<vector<int>> &d, vector<int> &t) {
    int n = d.size();
    vector<bool> visitat(n, false);
    vector<vector<int>> xij(n, vector<int>(n, 0));
    int tempsTotal = 0, actual = 0;
    visitat[actual] = true;
    cout << "Ruta de neteja: " << actual;

    while (tempsTotal < 480) { // 8 hores = 480 minuts
        int proxim = -1;
        int minDist = numeric_limits<int>::max();
       
        // Troba el pàrquing més proper no visitat
        
        for (int i = 0; i < n; ++i) {
            if (!visitat[i] && d[actual][i] < minDist && actual != i) {
                minDist = d[actual][i];
                proxim = i;
            }
        }
        
        if (proxim == -1 || tempsTotal + minDist + t[proxim] > 480-30) {
            break; // Si no es pot continuar, atura
        }
        
        tempsTotal += minDist + t[proxim];
        visitat[proxim] = true;
        xij[actual][proxim] = 1;
        actual = proxim;
        cout << " -> " << actual;
    }
    
    cout << "\nTemps total emprat: " << tempsTotal << " minuts + 30 minuts de tornar\n";
    
    cout << "\nMatriu Xij resultant:" << endl;
    for (const auto &row : xij) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
}

int main() {

    vector<vector<int>> d = {  {0, 5, 10, 2, 10}, 
                               {5, 0, 5,  7, 15}, 
                               {10, 5, 0, 15, 17}, 
                               {2, 7,  15, 0,  9}, 
                               {10, 15, 17, 9,0}} ; 

//    d = {                        {0, 5, 10, 2, 10, 3}, 
//                                 {5, 0, 5, 7, 15, 16}, 
//                                 {10, 5, 0, 15, 17, 15},
//                                 {2, 7, 15, 0, 9, 4}, 
//                                 {10, 15, 17, 9, 0, 10},
//                                 {8, 15, 11, 19, 5, 0}};

//       d = {
//         {0, 12, 25, 30, 14, 22, 35, 28, 18, 26},
//         {12, 0, 17, 22, 10, 15, 27, 20, 13, 19},
//         {25, 17, 0, 12, 18, 20, 15, 10, 22, 14},
//         {30, 22, 12, 0, 26, 29, 18, 15, 27, 21},
//         {14, 10, 18, 26, 0, 11, 22, 16, 8, 12},
//         {22, 15, 20, 29, 11, 0, 17, 13, 10, 8},
//         {35, 27, 15, 18, 22, 17, 0, 9, 19, 16},
//         {28, 20, 10, 15, 16, 13, 9, 0, 21, 12},
//         {18, 13, 22, 27, 8, 10, 19, 21, 0, 11},
//         {26, 19, 14, 21, 12, 8, 16, 12, 11, 0}
// };
    vector<int> t = {30, 120, 180, 60, 240, 110, 120, 180, 60, 240, 110};
    vector<string> etiquetes_t = {"0", "1", "2", "3", "4"};

    cout << "vector distàncies " << endl ;
    Output2DVectorInt(d);
    cout << endl << "vector temps de neteja" << endl;
    OutputVectorInt(t,etiquetes_t);
    cout << endl;

    netejaParkings(d, t);
    return 0;
}
