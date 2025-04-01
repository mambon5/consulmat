#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "crea_fitxer_opti.h"

using namespace std;

// g++ ../src/textProcess.cpp ../src/dates.cpp assign_coms_en_dies.cpp -o crea_fitx_lp

// com executar el fitxer lp en scip
// scip -f example.lp  > lp.out



void carregaDades( vector<vector<int>>& d,   vector<vector<int>>& rests, const int n) {

  // distancies de parquing "i" a parquing "j". dij.
  d = {
    {0, 13, 69, 480, 9, 7, 7},
    {13, 0, 78, 420, 9, 17, 17},
    {69, 78, 0, 480, 78, 64, 64},
    {480, 420, 480, 0, 480, 480, 480},
    {9, 9, 78, 480, 0, 16, 16},
    {7, 17, 64, 480, 16, 0, 1},
    {7, 17, 64, 480, 16, 1, 0}
};

// frequencia de cada comunitat
vector<int> fq = {5, 6, 4, 3, 1, 3, 2};

   //f a optimitzar:
   vector< vector< vector<int>>> objec_y(6, d); // aquí van les variables Yi,j,k
   vector< vector<int>> objec_x(6, vector<int>(n, 0)); // aqui van les xi,k
       // 6 capes (una per dia) on cada dia te les distàncies

vector<int> objectiu = flattenMatrix_ndim(objec_y);
vector<int> objectiu_x = flattenMatrix_ndim(objec_x);

// Afegim els elements de v2 al final de v1
objectiu.insert(objectiu.end(), objectiu_x.begin(), objectiu_x.end());

cout << "F objectiu (coeficients):" << endl;
for (int num : objectiu) cout << num << " ";
  cout << endl;

  // restriccions:
  vector<int> res1(n*n); 
  // for (int i = 0; i < n; ++i) {
  //     for (int j = 0; j < n; ++j) {
  //         res1[i*n+j] = d[i][j]+t[j];
  //     }
  // }
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

      
      
      
      rests = {res1,res2,res3,res4,res5,res6,res7,res8,
      res9,res10,res11,res12,res13,res14,res15,res16,res17,res18,res19,res20,
      res21,res22,res23,res24,res25, res26};
}



void fesOpti(int n) {

    
  vector<vector<int>> d;            // matriu distàncies
  vector<int> t;                    //vector temps de neteja
  vector<vector<int>> restriccions; // matriu restriccions
  carregaDades(d, restriccions, n); // carrega les dades


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
  write_lp(variables,objective_coeffs, constraints, au, al, bndl, bndu);

}



int main() {
  // int n = 5;// numero de parquings (comptant la base)
  // fesOpti(n);
  vector<vector<int>> matrix2D = {{1, 2, 3}, {4, 5, 6}};
  vector<vector<vector<int>>> matrix3D = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}};
  vector<vector<vector<vector<int>>>> matrix4D = {{{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}}};
  
  vector<int> flat2D = flattenMatrix_ndim(matrix2D);
  vector<int> flat3D = flattenMatrix_ndim(matrix3D);
  vector<int> flat4D = flattenMatrix_ndim(matrix4D);
  
  for (int num : flat2D) cout << num << " ";
  cout << endl;
  for (int num : flat3D) cout << num << " ";
  cout << endl;
  for (int num : flat4D) cout << num << " ";
  cout << endl;
   
  vector<vector<int>> d;
  vector<vector<int>> rests;
  int n = 7;
  carregaDades( d,  rests, n);
  
  
  return 0;
}