#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

// scip -f example.lp  > lp.out

int main() {
    // Definició de coeficients de la funció objectiu
    vector<double> objective_coeffs = {1, 2, 3, 1};
    vector<string> variables = {"x1", "x2", "x3", "x4"};

    // Matriu de restriccions (coeficients)
    vector<vector<double>> constraints = {
        {-1, 1, 1,  10},
        {-1, 1, 1,  10},
        { 1,-3, 1,   0},
        { 0, 1, 0, -3.5}
    };
    
    // Termes independents de les restriccions
    vector<double> rhs = {0, 20, 30, 0};
    vector<string> constraint_signs = {">=", "<=", "<=", "="};
    
    // Límits de les variables
    vector<pair<double, double>> bounds = {{0, 40}, {-1e20, 1e20}, {-1e20, 1e20}, {2, 3}};

    // Crear i escriure el fitxer LP
    ofstream lp_file("problem.lp");
    
    lp_file << "Minimize\n obj: ";
    for (size_t i = 0; i < objective_coeffs.size(); i++) {
        if (i > 0) lp_file << " + ";
        lp_file << objective_coeffs[i] << " " << variables[i];
    }
    lp_file << "\nSubject To\n";
    
    for (size_t i = 0; i < constraints.size(); i++) {
        lp_file << " c" << (i + 1) << ": ";
        for (size_t j = 0; j < constraints[i].size(); j++) {
            if (j > 0) lp_file << " + ";
            lp_file << constraints[i][j] << " " << variables[j];
        }
        lp_file << " " << constraint_signs[i] << " " << rhs[i] << "\n";
    }
    
    lp_file << "Bounds\n";
    for (size_t i = 0; i < bounds.size(); i++) {
        lp_file << " " << bounds[i].first << " <= " << variables[i] << " <= " << bounds[i].second << "\n";
    }
    
    lp_file << "General\n";
    for (const auto& var : variables) {
        lp_file << " " << var << "\n";
    }
    
    lp_file << "End\n";
    
    lp_file.close();
    cout << "Fitxer problem.lp generat correctament!" << endl;
    return 0;
}