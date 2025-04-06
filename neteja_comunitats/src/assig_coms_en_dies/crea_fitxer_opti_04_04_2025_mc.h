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

void escriure_obj(const string nom_fitxer, const vector<string> & variables, const vector<int> & objective_coeffs, 
  bool print=false) {
  ofstream lp_file(nom_fitxer );

  bool first = true;

  lp_file << "Minimize\n obj: ";
  for (size_t i = 0; i < variables.size(); i++) {
    if( objective_coeffs[i] != 0) { // si el coeficients es 0 no escriguis res
      if (first) first = false;
      else  lp_file << " + ";
      lp_file << objective_coeffs[i] << " " << variables[i];
      if(print) cout << "coeff[" << i << "]: " << objective_coeffs[i] <<   " var: " << variables[i] << endl;
    }
  }

  lp_file << "\nSubject To\n";
  lp_file.close();
}

void escriu_rest(const string nom_fitxer, const vector<string> & variables, 
  const vector<int> & restriccio, int b, int geq_leq_eq=2, bool print=false) {
    // geq_leq_both_eq es 0 si només hi ha la <=, 1 o leq  si >=, 2 o eq si =
    ofstream lp_file(nom_fitxer, ios::app);

    bool first = true;
   
    lp_file << " c" << ": ";
    for (size_t j = 0; j < restriccio.size(); j++) {
        if( restriccio[j] != 0) {
            if (first) first = false;
            else  lp_file << " + ";
            lp_file <<restriccio[j] << " " << variables[j];
        }
    }
    // restricció d'igualtat:
    if(geq_leq_eq == 2)    lp_file << " = " << b << "\n";
    
    // restricció de mes petit o igual:
    else if(geq_leq_eq == 1)    lp_file << " <= " << b << "\n";
    
  // restricció de mes gran o igual
    else if(geq_leq_eq == 0) lp_file << " >= " << b << "\n";

    else {
      cout << "error en escriu_rest(): en la tria del tipus de restricció";
    }

    lp_file.close();
}

void escriu_bounds(const string nom_fitxer, const vector<string> & variables, 
  const vector<double> & bndl, const vector<double> & bndu, bool print=false) {
    ofstream lp_file(nom_fitxer, ios::app);
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

void write_lp(const vector<string> & variables, const vector<int> & objective_coeffs,
  const vector<vector<int>> & constraints, const vector<int> & au, const vector<int> & al,
  const vector<double> & bndl, const vector<double> & bndu, bool print=false) {
    // Crear i escriure el fitxer LP
    string nom_fitxer = "ass_coms_en_dies.lp"; 
    ofstream lp_file(nom_fitxer );

    bool first = true;

    lp_file << "Minimize\n obj: ";
    for (size_t i = 0; i < variables.size(); i++) {
      if( objective_coeffs[i] != 0) { // si el coeficients es 0 no escriguis res
        if (first) first = false;
        else  lp_file << " + ";
        lp_file << objective_coeffs[i] << " " << variables[i];
        if(print) cout << "coeff[" << i << "]: " << objective_coeffs[i] <<   " var: " << variables[i] << endl;
      }
    }
   
    lp_file << "\nSubject To\n";
    for (size_t i = 0; i < constraints.size(); i++) {
        first = true;
        lp_file << " c_up" << (i + 1) << ": ";
        for (size_t j = 0; j < constraints[i].size(); j++) {
            if( constraints[i][j] != 0) {
                if (first) first = false;
                else  lp_file << " + ";
                lp_file << constraints[i][j] << " " << variables[j];
            }
        }
        lp_file << " <= " << au[i] << "\n";
        
        first = true;
        lp_file << " c_lo" << (i + 1) << ": ";
        for (size_t j = 0; j < constraints[i].size(); j++) {
            if( constraints[i][j] != 0) {
                if (first) first = false;
                else  lp_file << " + ";
                lp_file << constraints[i][j] << " " << variables[j];
            }
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


  void llegir_dos_vectors(const string& nom_fitxer, vector<int>& col1, vector<int>& col2) {
    ifstream fitxer(nom_fitxer);
    if (!fitxer.is_open()) {
        throw runtime_error("No s'ha pogut obrir el fitxer");
    }

    string linia;
    while (getline(fitxer, linia)) {
        stringstream ss(linia);
        int val1, val2;
        if (ss >> val1 >> val2) {
            col1.push_back(val1);
            col2.push_back(val2);
        }
    }

    fitxer.close();
}