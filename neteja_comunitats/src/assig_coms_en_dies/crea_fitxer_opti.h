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
    vector<vector<string>> vars(n, vector<string>(n));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            vars[i][j] = 'x' + to_string(i) + to_string(j);
        }
    }
    vector<string> variables = flattenMatrixString(vars);
    vector<string> var_ordre = {"u1", "u2", "u3", "u4"};
    variables.insert( variables.end(), var_ordre.begin(), var_ordre.end() );
     
    return variables;
}

void write_lp(const vector<string> & variables, const vector<int> & objective_coeffs,
  const vector<vector<int>> & constraints, const vector<double> & au, const vector<double> & al,
  const vector<double> & bndl, const vector<double> & bndu) {
    // Crear i escriure el fitxer LP
    string nom_fitxer = "problem.lp"; 
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
