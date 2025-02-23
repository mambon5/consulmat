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
vector<vector<int>> subMatriu (int n, const vector<vector<int>>& A) {
   vector<vector<int>> subA(n, vector<int>(n)); // Matriu n x n inicialitzada
    
    for (int i = 0; i < n; i++) {   // Recórrer les primeres n files
        for (int j = 0; j < n; j++) { // Recórrer les primeres n columnes
            subA[i][j] = A[i][j];
        }
    }
    
    return subA;
}


vector<string> creaVars(int n) {
    vector<vector<string>> vars(n, vector<string>(n));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            vars[i][j] = 'x' + to_string(i) + ","+ to_string(j);
        }
    }
    vector<string> variables = flattenMatrixString(vars);
    vector<string> var_ordre(n-1);
     for (int j = 0; j < n-1; ++j) {
            var_ordre[j] = 'u' + to_string(j+1);
        }
    variables.insert( variables.end(), var_ordre.begin(), var_ordre.end() );
     
    return variables;
}

void carregaDades(int n, vector<vector<int>>& d,  vector<int>& t, vector<vector<int>>& A,
                vector<double>& al, vector<double>& au, vector<double>& bndl, 
                vector<double>& bndu) {

  // distancies de parquing "i" a parquing "j". dij.
        d = {
        {0, 12, 25, 30, 14, 22, 35, 28, 18, 26},
        {12, 0, 17, 22, 10, 15, 27, 20, 13, 19},
        {25, 17, 0, 12, 18, 20, 15, 10, 22, 14},
        {30, 22, 12, 0, 26, 29, 18, 15, 27, 21},
        {14, 10, 18, 26, 0, 11, 22, 16, 8, 12},
        {22, 15, 20, 29, 11, 0, 17, 13, 10, 8},
        {35, 27, 15, 18, 22, 17, 0, 9, 19, 16},
        {28, 20, 10, 15, 16, 13, 9, 0, 21, 12},
        {18, 13, 22, 27, 8, 10, 19, 21, 0, 11},
        {26, 19, 14, 21, 12, 8, 16, 12, 11, 0}
        };
  // distàncies de les variables d'ordre:
  vector<int> du(n,0); // les variables d'ordre tenen distància 0;

  d = subMatriu(n,d);
  d.push_back(du); 

    // temps en netejar el pàrquing "i", ti en minuts:
  t = { 30, 90, 120, 150, 180, 210, 120, 150, 90, 180, 
        210, 60, 150, 120, 90, 180, 90, 210, 150, 120};

  vector<vector<int>> mat_t(n, t);
  cout << "matriu dels temps" << endl;
  Output2DVectorInt(mat_t);
  // agafa només els n primers temps de neteja
  t = vector<int>(t.begin(), t.begin() + n); 

  // restriccions:

  // temps de neteja i viatge en total entre 5h i 8h
  vector<int> res1(n*n); 
  for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
          res1[i*n+j] = d[i][j]+t[j];
      }
  }
       
  
  // es surt 1 cop de la base (parquing 0)
  int q = 0;
  vector<int> res3(n*n);
  for (int i = 0; i < n; ++i) { // i per cada fila
      for (int j = 0; j < n; ++j) { // j per cada columna
          if(i==q && i != j) res3[i*n+j] = 1;
          else res3[i*n+j] = 0;
      }
    }

  // vector<int> res3 =  { 
  //             0, 1, 1, 1, 1, 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //             };

    // de cada pàrquing es surt com a molt 1 cop 
  vector<vector<int>> resTip1(n, vector<int>(n*n)); 
  for (int w = 0; w < n; ++w) { //w per cada parquing
    for (int i = 0; i < n; ++i) { // i per cada fila
      for (int j = 0; j < n; ++j) { // j per cada columna
          if(i==w && i != j) resTip1[w][i*n+j] = 1;
          else resTip1[w][i*n+j] = 0;
      }
    }
  }
  
    //  (parking 0)
  // vector<int> res4 =  { 
  //             0, 1, 1, 1, 1, 
  //             0, 0, 0,0, 0, 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //             };
  // //  (parking 1)
  // vector<int> res5 =  { 
  //             0, 0, 0,0, 0,
  //             1, 0, 1, 1, 1, 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0,0,
  //             0, 0, 0,0,0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //               };
  // //  (parking 2)
  // vector<int> res6 =  { 
  //             0, 0, 0,0, 0, 
  //             0, 0, 0,0, 0,
  //             1, 1, 0, 1, 1, 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //             };
  // //  (parking 3)
  // vector<int> res7 =  { 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             1, 1, 1, 0, 1, 
  //             0, 0, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //             };
  // //  (parking 4)
  // vector<int> res8 =  { 
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             0, 0, 0,0, 0,
  //             1, 1, 1, 1, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //             };

  // es surt la mateixa quantitat de cops que s'entra en cada pàrquing
   vector<vector<int>> resTip2(n, vector<int> (n*n)); 
  for (int w = 0; w < n; ++w) { //w per cada parquing
    for (int i = 0; i < n; ++i) { // i per cada fila
      for (int j = 0; j < n; ++j) { // j per cada columna
          if(i==w && i != j) resTip2[w][i*n+j] = 1;
          else if(i==w) resTip2[w][i*n+j] = 0;
          else if(j==w) resTip2[w][i*n+j] = -1;
      }
    }
  }
      //  (parking 0)
  // vector<int> res9 =  { 
  //               0, 1, 1, 1, 1, 
  //               -1, 0, 0, 0,0,
  //               -1, 0, 0,0, 0,
  //               -1, 0, 0,0, 0,
  //               -1, 0, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //               };
  //     //  (parking 1)
  // vector<int> res10 =  {
  //               0, -1, 0, 0, 0, 
  //               1, 0, 1, 1, 1, 
  //               0,-1, 0,0, 0,
  //               0,-1, 0,0, 0,
  //               0,-1, 0,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0
  //                 };
  
  //     //  (parking 2)
  //   vector<int> res11 =  { 
  //               0, 0,-1, 0, 0,  
  //               0, 0, -1, 0,0,
  //               1, 1, 0, 1, 1, 
  //               0, 0,-1,0, 0,
  //               0, 0,-1,0, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0 };
  
  //     //  (parking 3)
  //   vector<int> res12 =  {
  //               0, 0, 0,-1, 0,  
  //               0, 0, 0,-1, 0, 
  //               0, 0, 0,-1, 0, 
  //               1, 1, 1, 0, 1, 
  //               0, 0, 0,-1, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0};
  
  //     //  (parking 4)
  //   vector<int> res13 =  {
  //               0, 0, 0, 0, -1,  
  //               0, 0, 0, 0, -1, 
  //               0, 0, 0, 0, -1, 
  //               0, 0, 0, 0, -1, 
  //               1, 1, 1, 1, 0,
  //             // variables d'ordre; ui amb i€{1,..,n-1}
  //               0, 0, 0, 0};
  

      // evitar subcircuits, equacions (n-1)(n-2) equacions, on n és el nombre de pàrquings
      // comptant l'orígen.
      // equació subcircuits: ui - uj + n*xij <= n-1
      
    vector<vector<int>> resTip3; //minim 3 parquings
    for (int w = 1; w < n; ++w) { //w per cada parquing x[w][t] = x12 = x[0][1]
      for (int t = 1; t < n; ++t) { 
        
        if(w != t) {
          vector<int> res(n*n);
          vector<int> varOrd(n-1);
          for (int i = 1; i < n; ++i) { // i per cada fila
          for (int j = 1; j < n; ++j) { // j per cada columna
              if(i==w && t == j) res[i*n+j] = n;
              else res[i*n+j] = 0;
          }
          if(w==i) varOrd[i-1] = 1;
          else if(t==i) varOrd[i-1] = -1;
          else varOrd[i-1] = 0;
        }
        res.insert( res.end(), varOrd.begin(), varOrd.end() ); // afegim ultima fila de 0s
        cout << "afegint la restriccio de subcircuits per a x" << w << "." << t << "..." << endl;
        resTip3.push_back(res);
        }

      }
    }
      // // x12
      // vector<int> res14 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, n, 0,  0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           1,-1, 0, 0};
      // // x13
      // vector<int> res15 =  {
      //           0, 0, 0,  0,  0, 
      //           0, 0, 0, n,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           1, 0,-1, 0};
      // // x14
      // vector<int> res16 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0, 0,  n, 
      //           0, 0, 0, 0, 0, 
      //           0, 0, 0, 0, 0, 
      //           0, 0, 0, 0, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           1, 0, 0,-1};

      // // x21
      // vector<int> res17 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, n, 0, 0,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //         -1, 1, 0, 0};
      // // x23
      // vector<int> res18 =  {
      //           0, 0, 0, 0,  0,  
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, n,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0, 1,-1, 0};
      // // x24
      // vector<int> res19 =  {
      //           0, 0, 0, 0,  0,  
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  n, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0, 1, 0,-1};

      // // x31
      // vector<int> res20 =  {
      //           0, 0, 0, 0,  0,  
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, n, 0, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //         -1, 0, 1, 0};
      // // x32
      // vector<int> res21 =  {
      //           0, 0, 0, 0,  0,  
      //           0, 0, 0, 0,  0, 
      //           0, 0, 0, 0,  0, 
      //           0, 0, n, 0,  0, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0,-1, 1, 0};
      // // x34
      // vector<int> res22 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0, 0,  n, 
      //           0, 0, 0, 0,  0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0, 0, 1,-1};
      // // x41
      // vector<int> res23 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, n, 0,  0, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           -1, 0, 0, 1};
      // // x42
      // vector<int> res24 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, n,  0, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0,-1, 0, 1};
      // // x43
      // vector<int> res25 =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  n, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           0, 0,-1, 1};

      // Suma uij = n*(n+1)/2
      vector<int> res26(n*n + n-1,0);
       for(int i = n*n; i<n*n+n-1; ++i){
        res26[i] = 1;
       }
      //  =  {
      //           0, 0, 0,  0, 0,  
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0, 
      //           0, 0, 0,  0, 0,
      //           // variables d'ordre; ui amb i€{1,..,n-1}
      //           1, 1, 1, 1};

      A.push_back(res1);
      A.push_back(res3);
      for(int i=0;i<resTip1.size(); ++i) {
        A.push_back(resTip1[i]);
      }
      for(int i=0;i<resTip2.size(); ++i) {
        A.push_back(resTip2[i]);
      }
      for(int i=0;i<resTip3.size(); ++i) {
        A.push_back(resTip3[i]);
      }
      A.push_back(res26);

      // A = {res1,res2,res3,res4,res5,res6,res7,res8,
      // res9,res10,res11,res12,res13,res14,res15,res16,res17,res18,res19,res20,
      // res21,res22,res23,res24,res25, res26};


    // fita inferior i superior de les restriccions   
    
    // al = {300,1,0,0,0,0,0,0,0,0,0,0, -1e20,-1e20,-1e20,
    // -1e20,-1e20,-1e20,-1e20,-1e20, -1e20,-1e20,-1e20,-1e20, n*(n-1)/2};

    // au = {480,1,1,1,1,1,1,0,0,0,0,0, 
    // n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 ,n-1 , n*(n-1)/2};

    al = {400,1};
    au = {480,1};
    for(int i =0; i<n; ++i) {
      al.push_back(0);
      au.push_back(1);
    }
    for(int i =0; i<n; ++i) {
      al.push_back(0);
      au.push_back(0);
    }
     for(int i =0; i<(n-2)*(n-1); ++i) {
      al.push_back(-1e20);
      au.push_back(n-1);
    }
    al.push_back(n*(n-1)/2);
    au.push_back(n*(n-1)/2);
    
   
    // Límits de les variables
    bndl = {};
    bndu= {};
    for(int i =0; i<n; ++i) {
      for(int j =0; j<n; ++j) {
        bndl.push_back(0);
        if(i==j) bndu.push_back(0);
        else bndu.push_back(1);
      }
    }
    for(int j =0; j<n-1; ++j) {
        bndl.push_back(1);
        bndu.push_back(n-1);
      }
    // bndl = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1};
    // bndu = {0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0, n-1,n-1,n-1,n-1};

}

void fesOpti(int n) {
     
    vector<vector<int>> d;            // matriu distàncies
    vector<int> t;                    //vector temps de neteja
    vector<vector<int>> A; // matriu restriccions A      
    vector<double> al; // fita superior de les restriccions
    vector<double> au; // fita inferior de les restriccions
    // al < A < au
    
    // Límits de les variables
    vector<double> bndl;
    vector<double> bndu;
    // bndl < X < bndu

    carregaDades(n, d, t, A, al, au, bndl, bndu); // carrega les dades

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
    vector<vector<int>> constraints = A;
    
    // Crear i escriure el fitxer LP
    string nom_fitxer = "problem_big.lp"; 
    ofstream lp_file(nom_fitxer);
    
    lp_file << "Minimize\n obj: ";
    for (size_t i = 0; i < objective_coeffs.size(); i++) {
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
  int n = 10;// numero de parquings (comptant la base)
  fesOpti(n);
   return 0;
}