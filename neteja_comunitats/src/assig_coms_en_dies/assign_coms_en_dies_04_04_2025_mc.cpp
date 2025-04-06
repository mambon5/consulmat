#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "crea_fitxer_opti_04_04_2025.h"

using namespace std;

// g++ ../src/textProcess.cpp ../src/dates.cpp assign_coms_en_dies.cpp -o crea_fitx_lp

// com executar el fitxer lp en scip
// scip -f ass_coms_en_dies.lp  > lp.out

vector<int> ajunta_vects_int(const vector<vector<vector<int>>> &v, const vector<vector<int>>& w) {
  vector<int> res = flattenMatrix_ndim_int(v);
  vector<int> pla_w = flattenMatrix_ndim_int(w);
  res.insert(res.end(), pla_w.begin(), pla_w.end());
  return res;
}


void Crea_lp(const int n, string nom_fitxer, bool print=false) {

    // distancies a peu de parquing "i" a parquing "j". dij.
    vector<vector<int>> d = read_csv_to_matrix_int("../../output/MDistPeu_2025-03-19.csv");
    d = submatriu_superior_esquerra(d, n);

  if(d[0].size() != n) {
    cout << "Error en carregaDades(): la quantitat de files de la matriu distàncies no es n:" << n << endl;
    return;
  }
  // frequencia de cada comunitat
  // llegint les E's i V's de cada comunitat
  vector<int> Es,Vs;
  llegir_dos_vectors("../../input/Es_i_Vs.txt", Es,Vs); 
  vector<int> fq = suma_vectors(Es, Vs); // calculant les frequències de cada comunitat (sumar E+V)
  fq = vector<int>(fq.begin(), fq.begin() + n); // primers n elements del vector només
  cout << "frequències: " << endl;
  OutputVectorInt(fq);


  // crea les variables:
  vector<string> variables = creaVars(n);
  if(print) {
    cout << "variables:" << endl;
    OutputVector(variables);
  }


  //f a optimitzar:
  vector<int>  coef_objectiu;
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

  // escriure funcio objectiu a minimitzar:
  escriure_obj(nom_fitxer, variables, coef_objectiu);

  // restriccions:
  // restricció AND:
  vector< vector< vector<int>>> empty_y(6, vector< vector<int>>(n,vector<int>(n,0))); // aquí van les variables Yi,j,k
  vector< vector<int>> empty_x(6, vector<int>(n, 0)); // aqui van les xi,k

  // vector<vector<int>> restriccions; // 6*n*n restriccions amb 6*n*n coefficients
                                      // cadascuna
  vector< vector< vector<int>>> restri_y = empty_y;
  vector< vector<int>> restri_x = empty_x; // inicialitzem la restriccio que anem a afegir
  vector<int> restri;
  cout << "apuntant restriccions" <<endl;
  for(int k=0; k<6; ++k) {
    for(int i=0; i<n; ++i) {
      for(int j=0; j<n; ++j) {
        if(print) cout << "restri " << i <<  ", " << j <<  "," << k <<endl;
        // a cada combinació diferent de "i, j, k" hi ha una restricció nova:
        // primera restricció del AND:
        restri_y[k][i][j] = 1;
        restri_x[k][i] = -1;
        restri = ajunta_vects_int(restri_y, restri_x);
        // restriccions.push_back(restri);
        escriu_rest(nom_fitxer,variables,restri,0,1);
        // segona restricció del AND:
        restri_x = empty_x;
        restri_x[k][j] = -1;
        restri = ajunta_vects_int(restri_y, restri_x);
        // restriccions.push_back(restri);
        escriu_rest(nom_fitxer,variables,restri,0,1);
        // tercera restricció del AND:
        restri_x[k][j] =  1;
        restri_x[k][i] =  1;
        restri_y[k][i][j] = -1;
        restri = ajunta_vects_int(restri_y, restri_x);
        // restriccions.push_back(restri);
        escriu_rest(nom_fitxer,variables,restri,1,1);

        //reinicia les restriccions
        restri_x = empty_x;
        restri_y = empty_y;

      }
    }
  }

  //reinicia les restriccions
  restri_x = empty_x;
  restri_y = empty_y;


  // restriccions freqüència:
  for(int i =0; i<n; ++i) {
    if(fq[i] == 6) {
      for(int k =0; k<6; ++k) {
        restri_x[k][i] = 1;
        restri = ajunta_vects_int(restri_y, restri_x);
        // restriccions.push_back(restri);
        escriu_rest(nom_fitxer,variables,restri,1,2);
        // au.push_back(1);
        // al.push_back(1);
        restri_x = empty_x;

      }
    }
    else if(fq[i] == 5) {
      for(int k =0; k<5; ++k) {
        restri_x[k][i] = 1;
        restri = ajunta_vects_int(restri_y, restri_x);
        // restriccions.push_back(restri);
        // au.push_back(1);
        // al.push_back(1);
        escriu_rest(nom_fitxer,variables,restri,1,2);
        restri_x = empty_x;

      }
      restri_x[5][i] = 1;
      restri = ajunta_vects_int(restri_y, restri_x);
      // restriccions.push_back(restri);
      // au.push_back(0);
      // al.push_back(0);
      escriu_rest(nom_fitxer,variables,restri,0,2);
      restri_x = empty_x;
    }

    else if(fq[i] == 3) {
      for(int k =0; k<6; ++k) {
        if(k % 2 == 0) {
          restri_x[k][i] = 1;
          restri = ajunta_vects_int(restri_y, restri_x);
          // restriccions.push_back(restri);
          // au.push_back(1);
          // al.push_back(1);
          escriu_rest(nom_fitxer,variables,restri,1,2);
          restri_x = empty_x;
        }
        else {
          restri_x[k][i] = 1;
          restri = ajunta_vects_int(restri_y, restri_x);
          // restriccions.push_back(restri);
          // au.push_back(0);
          // al.push_back(0);
          escriu_rest(nom_fitxer,variables,restri,0,2);
          restri_x = empty_x;
        }
        

      }
      
    }

    else { // si les comunitats es visiten 1,2,4 cops a la setmana.
      for(int k =0; k<5; ++k) { // menys dissabtes
        restri_x[k][i] = 1;
      }
      restri = ajunta_vects_int(restri_y, restri_x);
      // restriccions.push_back(restri);
      // au.push_back(fq[i]);
      // al.push_back(fq[i]);
      escriu_rest(nom_fitxer,variables,restri,fq[i],2);
      restri_x = empty_x;

      restri_x[5][i] = 1;
      restri = ajunta_vects_int(restri_y, restri_x);
      // restriccions.push_back(restri);
      // au.push_back(0);
      // al.push_back(0);
      escriu_rest(nom_fitxer,variables,restri,0,2);
      restri_x = empty_x;
    }
  }

  // Límits de les variables
  vector<double> bndl (6*n*(n+1),0); // limit inferior
  vector<double> bndu (6*n*(n+1),1); // limit superior
  escriu_bounds(nom_fitxer,variables,bndl, bndu);

}



// void fesOpti(int n, bool print=false) {
  
//   vector<vector<int>> d;            // matriu distàncies
//   vector<int> t;                    //vector temps de neteja
//   vector<vector<int>> restriccions; // matriu restriccions
//   vector<int> objective_coeffs;     // coeficients funció objectiu
//   vector<int> au (6*n*n*3,0);       // fites superiors de les restris
//   // fita superior de les restriccions  
//   for(int i =0; i<au.size(); ++i) {
//     if(i % 3 == 2) au[i] = 1;
//   }
//   vector<int> al (6*n*n*3, -std::numeric_limits<double>::infinity() ); // fites inf de les restris
//   carregaDades(d, restriccions, n, objective_coeffs, au, al); // carrega les dades


//   cout << "n: " << n << endl;
//   cout << "vector distàncies:  " << endl;
//   Output2DVectorInt(d);

//   // Definició de coeficients de la funció objectiu
//   // crea les variables:
//   vector<string> variables = creaVars(n);
//   if(print) {
//     cout << "variables:" << endl;
//     OutputVector(variables);
//   }

//   // Matriu de restriccions (coeficients)
//   vector<vector<int>> constraints = restriccions;

//     int m = constraints.size();

//   // Límits de les variables
  // vector<double> bndl (6*n*(n+1),0); // limit inferior
  // vector<double> bndu (6*n*(n+1),1); // limit superior

//   // Crear i escriure el fitxer LP
//   write_lp(variables,objective_coeffs, constraints, au, al, bndl, bndu);

// }



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
   

  int n = 15;
  
  vector<string> vars = creaVars(3);
  cout << "variables: " << endl;
  OutputVector(vars);
  string nom_fitxer = "ass_coms_en_dies.lp"; 

  
  Crea_lp(n, nom_fitxer);

  return 0;
}