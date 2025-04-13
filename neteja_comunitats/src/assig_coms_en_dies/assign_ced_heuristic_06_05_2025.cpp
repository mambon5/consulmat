#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include "../textProcess.h"
#include "../matrix_helper.h"

using namespace std;

// g++ ../textProcess.cpp ../dates.cpp assign_ced_heuristic_06_05_2025.cpp -o assign_heur -lcurl

vector<double> lats ;
vector<double> lons;
// Funció per calcular la variància d'un vector
double calcular_variancia(const vector<double>& valors) {
    if (valors.empty()) return 0.0;

    double mitjana = 0.0;
    for (double v : valors) mitjana += v;
    mitjana /= valors.size();

    double var = 0.0;
    for (double v : valors) var += (v - mitjana) * (v - mitjana);
    return var / valors.size();
}

// Funció per crear un subvector a partir d'un vector double segons els índexs
vector<double> crearSubvector(const vector<double>& original, const vector<int>& indexos) {
    vector<double> subvector;
    
    // Iterem sobre els índexs i afegim els valors corresponents al subvector
    for (int idx : indexos) {
        if (idx >= 0 && idx < original.size()) {
            subvector.push_back(original[idx]);
        }
    }
    
    return subvector;
}

// Funció per calcular la suma de variància de lat i lon
double var_diaria(const vector<double>& lats, const vector<double>& lons) {
    return calcular_variancia(lats) + calcular_variancia(lons);
}
double var_diaria_2(vector<int> comunitats, const vector<double>& lats, const vector<double>& lons) {
    vector<double> sublats = crearSubvector(lats, comunitats);
    vector<double> sublons = crearSubvector(lons, comunitats);
    return calcular_variancia(sublats) + calcular_variancia(sublons);
}

// Funció per calcular la suma de variància de cada dia junt
double var_setmana(const vector<vector<double>>& lats_dia, const vector<vector<double>>& lons_dia, bool print = false) {
    double var = 0;
    for(int i = 0; i<5; ++i) {
        vector<double> lat = lats_dia[i];
        vector<double> lon = lons_dia[i];
        var += var_diaria(lat, lon); 
        if(print) cout << "variança dia " << i << " : " << var_diaria(lat, lon) << endl;

    }
    
    return var;
}

// aqui lats i lons totals, farem un subector amb les del dia nomes
double var_setmana_2(const vector<vector<int>> comunitats_per_dia, vector<double> lats, vector<double> lons) {
    double var = 0;
    
    for(vector<int>dia : comunitats_per_dia) {
        var += var_diaria_2(dia, lats, lons);
    }
    return var;
}

vector<int> ordena_indexos(vector<int> & fq, vector<double> & lat, vector<double> & lon) {
    // Crear un vector d'índexs associats a la freqüència
    vector<int> indices(fq.size());
    for (int i = 0; i < fq.size(); ++i) {
        indices[i] = i;  // Inicialitzem el vector d'índexs amb els valors de 0 a n-1
    }

    // Ordenem els índexs en funció de la freqüència (freq 5, 3, 2, 1, 4)
    sort(indices.begin(), indices.end(), [&fq](int a, int b) {
        return fq[a] > fq[b];  // Ordena segons la freqüència (ordre descendent)
    });

    // Creamos els nous vectors ordenats basats en l'ordre d'índexs
    vector<int> fq_ordenat(fq.size());
    vector<double> lat_ordenat(lat.size());
    vector<double> lon_ordenat(lon.size());

    // Reordena els vectors fq, lat, lon segons els índexs ordenats
    for (int i = 0; i < fq.size(); ++i) {
        fq_ordenat[i] = fq[indices[i]];
        lat_ordenat[i] = lat[indices[i]];
        lon_ordenat[i] = lon[indices[i]];
    }

    fq = fq_ordenat;
    lat = lat_ordenat;
    lon = lon_ordenat;

    cout << "vectors ordenats segons criteri 5 -> 3 -> 2 -> 1 -> 4" << endl;
    return indices;
}

vector<vector<int>> distribueix_ced(int n) {

    // frequencia de cada comunitat
    // llegint les E's i V's de cada comunitat
    vector<int> Es,Vs;
    llegir_dos_vectors("../../input/Es_i_Vs.txt", Es,Vs); 
    vector<int> fq = suma_vectors(Es, Vs); // calculant les frequències de cada comunitat (sumar E+V)
    fq = vector<int>(fq.begin(), fq.begin() + n); // primers n elements del vector només
    cout << "frequències: " << endl;
    OutputVectorInt(fq);
    // lat i lon:
    string lat_lon_file = "../../input/Comunidades_coords.csv";

    
    llegir_lat_lon(lat_lon_file, lats, lons); 
    // escurcem els vectors lat i lon per tenir només n comunitats:
    lats = vector<double>(lats.begin(), lats.begin() + n);
    lons = vector<double>(lons.begin(), lons.begin() + n);
    OutputVectorDouble(lats);
    OutputVectorDouble(lons);

    vector<double> latitud = lats;
    vector<double> longitud = lons;
    // ordenem frequencies i latitud, lon, segons el criteri
    vector<int> indices = ordena_indexos(fq, latitud, longitud);
    cout << "reordre dels index: " << endl;
    OutputVectorInt(indices);
    OutputVectorInt(fq);
    OutputVectorDouble(latitud);
    OutputVectorDouble(longitud);

    const int num_dies = 5; // Dilluns a Divendres

    // Vector per cada dia de la setmana (index 0: dilluns, ..., 4: divendres)
    vector<vector<int>> comunitats_per_dia(num_dies);

    // També guardem les coordenades per dia per calcular la variància
    vector<vector<double>> lats_per_dia(num_dies);
    vector<vector<double>> lons_per_dia(num_dies);

    for (int i = 0; i < n; ++i) {
        int freq = fq[i];

        if (freq == 5) {
            // Assignem a tots els dies
            for (int d = 0; d < num_dies; ++d) {
                comunitats_per_dia[d].push_back(indices[i]);
                lats_per_dia[d].push_back(latitud[i]);
                lons_per_dia[d].push_back(longitud[i]);
            }
        } else if (freq == 4) {
            // Assignem 4 dies a la comunitat. Considerem les 4 combinacions possibles
            vector<vector<int>> combinacions_dies = {
                {0, 1, 3, 4},  // Dilluns, Dimarts, Dijous, Divendres
                {0, 1, 2, 4},  // Dilluns, Dimarts, Dimecres, Divendres
                {0, 2, 3, 4},  // Dilluns, Dimecres, Dijous, Divendres
                {1, 2, 3, 4}   // Dimarts, Dimecres, Dijous, Divendres
            };
            
            // Variables per guardar la millor combinació i la menor variància
            double millor_variancia = numeric_limits<double>::max();
            vector<int> millor_combinacio;
        
            // Mirem quina combinació redueix més la variància
            for (const auto& combinacio : combinacions_dies) {
                // Afegim temporalment les comunitats als 4 dies i calculem la variància
                for (int dia : combinacio) {
                    lats_per_dia[dia].push_back(latitud[i]);
                    lons_per_dia[dia].push_back(longitud[i]);
                }
        
                // Calculem la variància total per a aquesta combinació de dies
                double var_total = var_setmana(lats_per_dia, lons_per_dia);
                
        
                // Si la variància és millor (menor), guardem aquesta combinació
                if (var_total < millor_variancia) {
                    millor_variancia = var_total;
                    millor_combinacio = combinacio;
                }
        
                // Traiem la comunitat de les llistes per tornar a provar el següent parell
                for (int dia : combinacio) {
                    lats_per_dia[dia].pop_back();
                    lons_per_dia[dia].pop_back();
                }
            }
        
            // Assignem la comunitat a la millor combinació de dies
            for (int dia : millor_combinacio) {
                comunitats_per_dia[dia].push_back(indices[i]);
                lats_per_dia[dia].push_back(latitud[i]);
                lons_per_dia[dia].push_back(longitud[i]);
            }
        } else if (freq == 3) {
            // Assignem dilluns, dimecres, divendres (0, 2, 4)
            for (int d : {0, 2, 4}) {
                comunitats_per_dia[d].push_back(indices[i]);
                lats_per_dia[d].push_back(latitud[i]);
                lons_per_dia[d].push_back(longitud[i]);
            }
        } else if (freq == 2) {
            // Assignem dilluns i dijous (0, 3) o dimarts i divendres (1, 4)
            vector<vector<int>> parells_dies = {{0, 3}, {1, 4}};
            
            // Variables per guardar la millor combinació i la menor variància
            double millor_variancia = numeric_limits<double>::max();
            vector<int> millor_parell;
        
            // Mirem quin parell redueix més la variància
            for (const auto& parell : parells_dies) {
                int dia1 = parell[0];
                int dia2 = parell[1];
        
                // Afegim temporalment les comunitats als dos dies i calculem la variància
                lats_per_dia[dia1].push_back(latitud[i]);
                lons_per_dia[dia1].push_back(longitud[i]);
                lats_per_dia[dia2].push_back(latitud[i]);
                lons_per_dia[dia2].push_back(longitud[i]);
        
                // Calculem la variància total per a aquesta combinació de dies
                double var_total = var_setmana(lats_per_dia,lons_per_dia);
        
                // Si la variància és millor (menor), guardem aquest parell
                if (var_total < millor_variancia) {
                    millor_variancia = var_total;
                    millor_parell = parell;
                }
        
                // Traiem la comunitat de les llistes per tornar a provar el següent parell
                lats_per_dia[dia1].pop_back();
                lons_per_dia[dia1].pop_back();
                lats_per_dia[dia2].pop_back();
                lons_per_dia[dia2].pop_back();
            }
        
            // Assignem la comunitat al millor parell de dies
            int dia1 = millor_parell[0];
            int dia2 = millor_parell[1];
        
            // Assignem definitivament la comunitat als dies seleccionats
            comunitats_per_dia[dia1].push_back(indices[i]);
            lats_per_dia[dia1].push_back(latitud[i]);
            lons_per_dia[dia1].push_back(longitud[i]);
        
            comunitats_per_dia[dia2].push_back(indices[i]);
            lats_per_dia[dia2].push_back(latitud[i]);
            lons_per_dia[dia2].push_back(longitud[i]);
        
        } else if (freq == 1) {
            // Busquem el dia que minimitza la variància total
            double millor_var = numeric_limits<double>::max();
            int millor_dia = -1;

            for (int d = 0; d < num_dies; ++d) {
                // Provem afegir-hi aquesta comunitat
                lats_per_dia[d].push_back(latitud[i]);
                lons_per_dia[d].push_back(longitud[i]);

                double var = var_setmana(lats_per_dia, lons_per_dia);

                // Traiem l’últim que havíem afegit
                lats_per_dia[d].pop_back();
                lons_per_dia[d].pop_back();

                if (var < millor_var) {
                    millor_var = var;
                    millor_dia = d;
                }
            }

            // Assignem definitivament la comunitat al millor dia
            comunitats_per_dia[millor_dia].push_back(indices[i]);
            lats_per_dia[millor_dia].push_back(latitud[i]);
            lons_per_dia[millor_dia].push_back(longitud[i]);
        }
    }
    cout << endl << "variança total: " << var_setmana(lats_per_dia, lons_per_dia, true)<< endl;


    return comunitats_per_dia;
}

int main() {

    vector<vector<int>> coms_dia = distribueix_ced(350);
    const int num_dies = 5; // Dilluns a Divendres

    // Mostrar resultats
    vector<string> noms_dies = {"Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres"};
    for (int d = 0; d < num_dies; ++d) {
        cout << noms_dies[d] << ": ";
        for (int c : coms_dia[d]) {
            cout << c << " ";
        }
        cout << endl;
    }


    
    vector<vector<int>> comunitats_per_dia(5);

    // Assignem les comunitats a cada dia segons el resultat del model d'optimitzacio
    comunitats_per_dia[0] = {2, 4};    // Dilluns
    comunitats_per_dia[1] = {3, 4};    // Dimarts
    comunitats_per_dia[2] = {1, 4, 5, 6};    // Dimecres
    comunitats_per_dia[3] = {0, 1, 4};    // Dijous
    comunitats_per_dia[4] = {3, 4};    // Divendres
    cout << "variança del model d'optimització: " << var_setmana_2(comunitats_per_dia, lats, lons) <<endl;

    return 0;
}
