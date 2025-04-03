#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "../textProcess.h"
#include "../matrix_helper.h"

using namespace std;


// com executar el fitxer lp en scip
// scip -f example.lp  > lp.out

vector<string> creaVars(int n) {
    vector<vector<vector<string>>> vars_y(6, vector<vector<string>>(n,vector<string>(n)));
    
    for (int k = 0; k < 6; ++k) {
      for (int i = 0; i < n; ++i) {
          for (int j = 0; j < n; ++j) {
            vars_y[k][i][j] = "y" + to_string(k) + ","+ to_string(i) + ","+ to_string(j);
          }
      }
    }

    vector<vector<string>> vars_x(6,vector<string>(n));
    for (int k = 0; k < 6; ++k) {
      for (int j = 0; j < n; ++j) {
          vars_x[k][j] = "x"+ to_string(k) + ","+ to_string(j);
      }
    }

    vector<string> ap_y = flattenMatrix_ndim_str(vars_y);
    vector<string> ap_x = flattenMatrix_ndim_str(vars_x);

    // Afegim els elements de v2 al final de v1
    ap_y.insert(ap_y.end(), ap_x.begin(), ap_x.end());
    
     
    return ap_y;
}

void write_lp(const vector<string> & variables, const vector<int> & objective_coeffs,
  const vector<vector<int>> & constraints, const vector<double> & au, const vector<double> & al,
  const vector<double> & bndl, const vector<double> & bndu) {
    // Crear i escriure el fitxer LP
    string nom_fitxer = "ass_coms_en_dies.lp"; 
    ofstream lp_file(nom_fitxer);

    lp_file << "Minimize\n obj: ";
    for (size_t i = 0; i < variables.size(); i++) {
      if (i > 0) lp_file << " + ";
      lp_file << objective_coeffs[i] << " " << variables[i];
      cout << "coeff[" << i << "]: " << objective_coeffs[i] <<   " var: " << variables[i] << endl;
    }
    lp_file << "\nSubject To\n";
    for (size_t i = 0; i < constraints.size(); i++) {
      lp_file << " c_up" << (i + 1) << ": ";
      for (size_t j = 0; j < constraints[i].size(); j++) {
          if (j > 0) lp_file << " + ";
          lp_file << constraints[i][j] << " " << variables[j];
      }
      lp_file << " <= " << au[i] << "\n";

      lp_file << " c_lo" << (i + 1) << ": ";
      for (size_t j = 0; j < constraints[i].size(); j++) {
          if (j > 0) lp_file << " + ";
          lp_file << constraints[i][j] << " " << variables[j];
      }
      lp_file << " >= " << al[i] << "\n";
    }
    lp_file << "Bounds\n";
    for (size_t i = 0; i < bndl.size(); i++) {
      lp_file << " " << bndl[i] << " <= " << variables[i] << " <= " << bndu[i] << "\n";
    }
    // quines variables han de ser enteres:
    lp_file << "General\n";
    for (const auto& var : variables) {
      lp_file << " " << var << "\n";
    }

    lp_file << "End\n";

    lp_file.close();
    cout << "Fitxer " << nom_fitxer << " generat correctament!" << endl;
    }
