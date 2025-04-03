#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "crea_fitxer_opti.h"

using namespace std;

// g++ ../src/textProcess.cpp ../src/dates.cpp assign_coms_en_dies.cpp -o crea_fitx_lp

// com executar el fitxer lp en scip
// scip -f example.lp  > lp.out



void carregaDades( vector<vector<int>>& d,   vector<vector<int>>& rests, const int n, vector<int> & coef_objectiu) {

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

if(d[0].size() != n) {
  cout << "Error en carregaDades(): la quantitat de files de la matriu distàncies no es n:" << n << endl;
  return;
}
// frequencia de cada comunitat
vector<int> fq = {5, 6, 4, 3, 1, 3, 2};

//f a optimitzar:
vector< vector< vector<int>>> objec_y(6, d); // aquí van les variables Yi,j,k
vector< vector<int>> objec_x(6, vector<int>(n, 0)); // aqui van les xi,k
    // 6 capes (una per dia) on cada dia te les distàncies

vector<int> objectiu = flattenMatrix_ndim_int(objec_y);
vector<int> objectiu_x = flattenMatrix_ndim_int(objec_x);

// Afegim els elements de v2 al final de v1
objectiu.insert(objectiu.end(), objectiu_x.begin(), objectiu_x.end());
coef_objectiu = objectiu;

cout << "F objectiu (coeficients):" << endl;
for (int num : objectiu) cout << num << " ";
  cout << endl;

  // // restriccions:
  // vector<int> res1(n*n); 
  // // for (int i = 0; i < n; ++i) {
  // //     for (int j = 0; j < n; ++j) {
  // //         res1[i*n+j] = d[i][j]+t[j];
  // //     }
  // // }
  //   // variables d'ordre; ui amb i€{1,..,n-1}
  //   vector<int> vars_ord = {0,0,0,0};
  //   res1.insert( res1.end(), vars_ord.begin(), vars_ord.end() );
                
  //             // que sumin tots els temps de viatge pel seu temps de neteja, més de 5h'
  // vector<int> res2 =  res1;
  
  // // es surt 1 cop de la base (parquing 0)
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
    //  (parking 0)
  
      
      // rests = {res1,res2,res3,res4,res5,res6,res7,res8,
      // res9,res10,res11,res12,res13,res14,res15,res16,res17,res18,res19,res20,
      // res21,res22,res23,res24,res25, res26};
}



void fesOpti(int n) {
  
  vector<vector<int>> d;            // matriu distàncies
  vector<int> t;                    //vector temps de neteja
  vector<vector<int>> restriccions; // matriu restriccions
  vector<int> objective_coeffs;     // coeficients funció objectiu
  carregaDades(d, restriccions, n, objective_coeffs); // carrega les dades

  cout << "n: " << n << endl;
  cout << "vector distàncies:  " << endl;
  Output2DVectorInt(d);

  // Definició de coeficients de la funció objectiu
  // crea les variables:
  vector<string> variables = creaVars(n);
  cout << "variables:" << endl;
  OutputVector(variables);
  // Matriu de restriccions (coeficients)
  vector<vector<int>> constraints = restriccions;

  // fita superior de les restriccions
  vector<double> al = {};
  // fita inferior de les restriccions
  vector<double> au = {};
  int m = constraints.size();

  // Límits de les variables
  vector<double> bndl (6*n*(n+1),0); // limit inferior
  vector<double> bndu (6*n*(n+1),1); // limit superior

  // Crear i escriure el fitxer LP
  write_lp(variables,objective_coeffs, constraints, au, al, bndl, bndu);

}



int main() {
  // int n = 5;// numero de parquings (comptant la base)
  // fesOpti(n);
  vector<vector<int>> matrix2D = {{1, 2, 3}, {4, 5, 6}};
  vector<vector<vector<int>>> matrix3D = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}};
  vector<vector<vector<vector<int>>>> matrix4D = {{{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}}};
  
  vector<int> flat2D = flattenMatrix_ndim_int(matrix2D);
  vector<int> flat3D = flattenMatrix_ndim_int(matrix3D);
  vector<int> flat4D = flattenMatrix_ndim_int(matrix4D);
  
  for (int num : flat2D) cout << num << " ";
  cout << endl;
  for (int num : flat3D) cout << num << " ";
  cout << endl;
  for (int num : flat4D) cout << num << " ";
  cout << endl;
   

  int n = 7;
  
  vector<string> vars = creaVars(3);
  cout << "variables: " << endl;
  OutputVector(vars);
  
  fesOpti(n);

  return 0;
}