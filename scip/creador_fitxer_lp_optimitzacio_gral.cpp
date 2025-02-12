#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "../src/textProcess.h"

using namespace std;

// g++ ../src/textProcess.cpp ../src/dates.cpp creador_fitxer_lp_optimitzacio.cpp -o crea_fitx_lp

// com executar el fitxer lp en scip
// scip -f example.lp  > lp.out



vector<int> flattenMatrix(const vector<vector<int>>& matrix) {
    vector<int> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}

vector<string> flattenMatrixString(const vector<vector<string>>& matrix) {
    vector<string> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}

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

void carregaDades( vector<vector<int>>& d,  vector<int>& t, vector<vector<int>>& rests) {

  // distancies de parquing "i" a parquing "j". dij.
  d = { { 0, 5, 10,  2, 10}, 
        {5,  0,  5,  7, 15}, 
        {10, 5, 0,  15, 17}, 
        {2,  7, 15,  0, 9}, 
        {10, 15, 17, 9, 0},
          // variables d'ordre:
          {0,0,0,0}} ;

    // temps en netejar el pàrquing "i", ti en minuts:
  t = {30, 120, 180, 60, 240};

  // restriccions:
  vector<int> res1(n*n); 
  for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
          res1[i*n+j] = d[i][j]+t[j];
      }
  }
    // variables d'ordre; ui amb i€{1,..,n-1}
    vector<int> vars_ord = {0,0,0,0};
    res1.insert( res1.end(), vars_ord.begin(), vars_ord.end() );
                
              // que sumin tots els temps de viatge pel seu temps de neteja, més de 5h'
  vector<int> res2 =  res1;
  
  // es surt 1 cop de la base (parquing 0)
  vector<int> res3 =  { 
              0, 1, 1, 1, 1, 
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
              };

    // de cada pàrquing es surt com a molt 1 cop 
    //  (parking 0)
  vector<int> res4 =  { 
              0, 1, 1, 1, 1, 
              0, 0, 0,0, 0, 
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
              };
  //  (parking 1)
  vector<int> res5 =  { 
              0, 0, 0,0, 0,
              1, 0, 1, 1, 1, 
              0, 0, 0,0, 0,
              0, 0, 0,0,0,
              0, 0, 0,0,0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
                };
  //  (parking 2)
  vector<int> res6 =  { 
              0, 0, 0,0, 0, 
              0, 0, 0,0, 0,
              1, 1, 0, 1, 1, 
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
              };
  //  (parking 3)
  vector<int> res7 =  { 
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              1, 1, 1, 0, 1, 
              0, 0, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
              };
  //  (parking 4)
  vector<int> res8 =  { 
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              0, 0, 0,0, 0,
              1, 1, 1, 1, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
              };

  // es surt la mateixa quantitat de cops que s'entra en cada pàrquing
      //  (parking 0)
  vector<int> res9 =  { 
                0, 1, 1, 1, 1, 
                -1, 0, 0, 0,0,
                -1, 0, 0,0, 0,
                -1, 0, 0,0, 0,
                -1, 0, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
                };
      //  (parking 1)
  vector<int> res10 =  {
                0, -1, 0, 0, 0, 
                1, 0, 1, 1, 1, 
                0,-1, 0,0, 0,
                0,-1, 0,0, 0,
                0,-1, 0,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0
                  };
  
      //  (parking 2)
    vector<int> res11 =  { 
                0, 0,-1, 0, 0,  
                0, 0, -1, 0,0,
                1, 1, 0, 1, 1, 
                0, 0,-1,0, 0,
                0, 0,-1,0, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0 };
  
      //  (parking 3)
    vector<int> res12 =  {
                0, 0, 0,-1, 0,  
                0, 0, 0,-1, 0, 
                0, 0, 0,-1, 0, 
                1, 1, 1, 0, 1, 
                0, 0, 0,-1, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0};
  
      //  (parking 4)
    vector<int> res13 =  {
                0, 0, 0, 0, -1,  
                0, 0, 0, 0, -1, 
                0, 0, 0, 0, -1, 
                0, 0, 0, 0, -1, 
                1, 1, 1, 1, 0,
              // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 0, 0};
  

      // evitar subcircuits, equacions (n-1)(n-2) equacions, on n és el nombre de pàrquings
      // comptant l'orígen.
      // equació subcircuits: ui - uj + n*xij <= n-1
      

      // x12
      vector<int> res14 =  {
                0, 0, 0,  0, 0,  
                0, 0, n, 0,  0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                1,-1, 0, 0};
      // x13
      vector<int> res15 =  {
                0, 0, 0,  0,  0, 
                0, 0, 0, n,  0, 
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                1, 0,-1, 0};
      // x14
      vector<int> res16 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0, 0,  n, 
                0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                1, 0, 0,-1};

      // x21
      vector<int> res17 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, n, 0, 0,  0, 
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
              -1, 1, 0, 0};
      // x23
      vector<int> res18 =  {
                0, 0, 0, 0,  0,  
                0, 0, 0, 0,  0, 
                0, 0, 0, n,  0, 
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0, 1,-1, 0};
      // x24
      vector<int> res19 =  {
                0, 0, 0, 0,  0,  
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  n, 
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0, 1, 0,-1};

      // x31
      vector<int> res20 =  {
                0, 0, 0, 0,  0,  
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0, 
                0, n, 0, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
              -1, 0, 1, 0};
      // x32
      vector<int> res21 =  {
                0, 0, 0, 0,  0,  
                0, 0, 0, 0,  0, 
                0, 0, 0, 0,  0, 
                0, 0, n, 0,  0, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0,-1, 1, 0};
      // x34
      vector<int> res22 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0, 0,  n, 
                0, 0, 0, 0,  0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0, 1,-1};
      // x41
      vector<int> res23 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, n, 0,  0, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                -1, 0, 0, 1};
      // x42
      vector<int> res24 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, n,  0, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0,-1, 0, 1};
      // x43
      vector<int> res25 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  n, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                0, 0,-1, 1};

      // Suma uij = n*(n+1)/2
      vector<int> res26 =  {
                0, 0, 0,  0, 0,  
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0, 
                0, 0, 0,  0, 0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                1, 1, 1, 1};

      
      
      
      vector<vector<int>> rests = {res1,res2,res3,res4,res5,res6,res7,res8,
      res9,res10,res11,res12,res13,res14,res15,res16,res17,res18,res19,res20,
      res21,res22,res23,res24,res25, res26};
}


void fesOpti(int n) {

     
    vector<vector<int>> d;            // matriu distàncies
    vector<int> t;                    //vector temps de neteja
    vector<vector<int>> restriccions; // matriu restriccions
    carregaDades(d, t, restriccions); // carrega les dades


    vector<int> dist = flattenMatrix(d);
    
    cout << "n: " << n << endl;
    cout << "vector distàncies:  " << endl;
    Output2DVectorInt(d);

    // Definició de coeficients de la funció objectiu
    vector<int> objective_coeffs = dist;
    // crea les variables:
    vector<string> variables = creaVars(n);
    cout << "variables:" << endl;
    OutputVector(variables);
    // Matriu de restriccions (coeficients)
    vector<vector<int>> constraints = restriccions;
    
    // fita superior de les restriccions
    vector<double> al = {-1e20,300,1,0,0,0,0,0,0,0,0,0,0, -1e20,-1e20,-1e20,
    -1e20,-1e20,-1e20,-1e20,-1e20, -1e20,-1e20,-1e20,-1e20, 10};
    // fita inferior de les restriccions
    vector<double> au = {480,1e20,1,1,1,1,1,1,0,0,0,0,0, 
    4,4,4,4,4,4,4,4,4,4,4,4, 10};
    int m = constraints.size();
   
    // Límits de les variables
    vector<double> bndl = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1};
    vector<double> bndu = {0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0, n-1,n-1,n-1,n-1};
    
    // Crear i escriure el fitxer LP
    string nom_fitxer = "problem_big.lp"; 
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

int main() {
  int n = 5;// numero de parquings (comptant la base)
  fesOpti(n);
   return 0;
}