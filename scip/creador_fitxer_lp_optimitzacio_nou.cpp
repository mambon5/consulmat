#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

// scip -f example.lp  > lp.out
vector<vector<string>> creaVars(int n) {
    vector<vector<string>> vars(n, vector<string>(n));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            vars[i][j] = "x" + to_string(i) + to_string(j);
        }
    }
     
    return flattenMatrixString(vars);;
}

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



void fesopti() {

     // distancies de parquing "i" a parquing "j". dij.
    vector<vector<int>> d = { {5, 10, 2, 10}, {5,5,7,15}, {10, 5, 15, 17}, 
                                {2, 7, 15, 9}, {10, 15, 17, 9},
                                // variables d'ordre:
                                {0,0,0,0}} ; 
    
     vector<int> dist = flattenMatrix(d);

    cout << "vector distàncies:  " << endl;
    Output2DVectorInt(d);
    int n = 5;
    // temps en netejar el pàrquing "i", ti en minuts:
    vector<int> t = {30, 120, 180, 60, 240};

    vector<int> res1 = { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3],
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                 };
                // que sumin tots els temps de viatge pel seu temps de neteja, més de 5h'
	vector<int> res2 =  { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3],
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };
    
    // es surt 1 cop de la base (parquing 0)
    vector<int> res3 =  { 
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };

     // de cada pàrquing es surt com a molt 1 cop 
     //  (parking 0)
    vector<int> res4 =  { 
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };
    //  (parking 1)
    vector<int> res5 =  { 
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                 };
    //  (parking 2)
    vector<int> res6 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };
    //  (parking 3)
    vector<int> res7 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };
    //  (parking 4)
    vector<int> res8 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                };

    // es surt la mateixa quantitat de cops que s'entra en cada pàrquing
        //  (parking 0)
   vector<int> res9 =  { 
                1, 1, 1, 1, 
                 -1, 0, 0,0,
                 -1, 0, 0,0,
                 -1, 0, 0,0,
                 -1, 0, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                 };
        //  (parking 1)
    vector<int> res10 =  {
                -1, 0, 0, 0, 
                  1, 1, 1, 1, 
                  0,-1, 0,0,
                  0,-1, 0,0,
                  0,-1, 0,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0
                   };
   
        //  (parking 2)
     vector<int> res11 =  { 
                0,-1, 0, 0, 
                  0,-1, 0,0,
                  1, 1, 1, 1, 
                  0, 0,-1,0,
                  0, 0,-1,0,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0 };
   
        //  (parking 3)
     vector<int> res12 =  {
                0, 0,-1, 0,  
                 0, 0,-1, 0, 
                 0, 0,-1, 0, 
                 1, 1, 1, 1, 
                 0, 0, 0,-1,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
   
        //  (parking 4)
     vector<int> res13 =  {
                 0, 0, 0, -1,  
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 1, 1, 1, 1,
                // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
   

        // evitar subcircuits, equacions (n-1)(n-2) equacions, on n és el nombre de pàrquings
        // comptant l'orígen.
        // equació subcircuits: ui - uj + n*xij <= n-1
        

        // x12
        vector<int> res14 =  {
                 0, 0, 0,  0,  
                 0, n, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  1,-1, 0, 0};
        // x13
        vector<int> res15 =  {
                 0, 0, 0,  0,  
                 0, 0, n,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  1, 0,-1, 0};
        // x14
        vector<int> res16 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  n, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  1, 0, 0,-1};

        // x21
        vector<int> res17 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, n, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                -1, 1, 0, 0};
        // x23
        vector<int> res18 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, n,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 1,-1, 0};
        // x24
        vector<int> res19 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  n, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 1, 0,-1};

        // x31
        vector<int> res20 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, n, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                -1, 0, 1, 0};
        // x32
        vector<int> res21 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, n,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0,-1, 1, 0};
        // x34
        vector<int> res22 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  n, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 1,-1};
        // x41
        vector<int> res23 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, n, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  -1, 0, 0, 1};
        // x42
        vector<int> res24 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, n,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0,-1, 0, 1};
        // x43
        vector<int> res25 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  n,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0,-1, 1};

        // Suma uij = n*(n+1)/2
        vector<int> res26 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  1, 1, 1, 1};

        // s'han de visitat totes les ciutats 1 cop:
        // x0
        vector<int> res27 =  {
                 1, 1, 1,  1,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x1
        vector<int> res28 =  {
                 0, 0, 0,  0,  
                 1, 1, 1,  1, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x2
        vector<int> res29 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 1, 1, 1,  1, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x3
        vector<int> res30 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 1, 1, 1,  1, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x4
        vector<int> res31 =  {
                 0, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  0, 
                 1, 1, 1,  1,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};

        // s'han de visitat totes les ciutats 1 cop:
        // x0
        vector<int> res32 =  {
                 0, 0, 0,  0,  
                 1, 0, 0,  0, 
                 1, 0, 0,  0, 
                 1, 0, 0,  0, 
                 1, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x1
        vector<int> res33 =  {
                 1, 0, 0,  0,  
                 0, 0, 0,  0, 
                 0, 1, 0,  0, 
                 0, 1, 0,  0, 
                 0, 1, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x2
        vector<int> res34 =  {
                 0, 1, 0,  0,  
                 0, 1, 0,  0, 
                 0, 0, 0,  0, 
                 0, 0, 1,  0, 
                 0, 0, 1,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x3
        vector<int> res35 =  {
                 0, 0, 1,  0,  
                 0, 0, 1,  0, 
                 0, 0, 1,  0, 
                 0, 0, 0,  0, 
                 0, 0, 0,  1,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        // x4
        vector<int> res36 =  {
                 0, 0, 0,  1,  
                 0, 0, 0,  1, 
                 0, 0, 0,  1, 
                 0, 0, 0,  1, 
                 0, 0, 0,  0,
                 // variables d'ordre; ui amb i€{1,..,n-1}
                  0, 0, 0, 0};
        
        
        vector<vector<int>> rests = {res1,res2,res3,res4,res5,res6,res7,res8,
        res9,res10,res11,res12,res13,res14,res15,res16,res17,res18,res19,res20,
        res21,res22,res23,res24,res25, res26, res27,res28,res29, res30, res31,
        res32,res33,res34, res35, res36};
        real_2d_array a =  convertMatToALGLIBFormat(res).c_str();
        real_1d_array al = "[-inf,180,1,0,0,0,0,0,0,0,0,0,0, -inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf, 10, 1,1,1,1,1, 1,1,1,1,1]";
        real_1d_array au = "[480,+inf,1,1,1,1,1,1,0,0,0,0,0, 4,4,4,4,4,4,4,4,4,4,4,4, 10, 1,1,1,1,1, 1,1,1,1,1]";
        real_1d_array c = convertVecToALGLIBFormat(dist).c_str();
        real_1d_array s =       "[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1]"; // escala de cada variable
        real_1d_array bndl =    "[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1]";
        real_1d_array bndu =    convertVecToALGLIBFormat(
                                { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, n-1,n-1,n-1,n-1}
        ).c_str();

    // Definició de coeficients de la funció objectiu
    vector<double> objective_coeffs = dist;
    int n = 4;
    
    <vector<string> variables = creaVars(n);
    // Matriu de restriccions (coeficients)
    vector<vector<double>> constraints = rests;
    constraints.insert(rests.end(), rests.begin(), rests.end());
    
    // Termes independents de les restriccions
    vector<double> al = {-1e20,180,1,0,0,0,0,0,0,0,0,0,0, -1e20,-1e20,-1e20,
    -1e20,-1e20,-1e20,-1e20,-1e20, -1e20,-1e20,-1e20,-1e20, 10, 
    1,1,1,1,1, 1,1,1,1,1};
    vector<double> au = {480,1e20,1,1,1,1,1,1,0,0,0,0,0, 
    4,4,4,4,4,4,4,4,4,4,4,4, 10, 1,1,1,1,1, 1,1,1,1,1};
    int m = constraints.size();
    vector<string> mesPetit(m, "<=");
    vector<string> mesGran(m, ">=");
    
    // Límits de les variables
    vector<pair<double, double>> bounds = {{0, 40}, {-1e20, 1e20}, 
    {-1e20, 1e20}, {2, 3}};

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
 
}

int main() {
    fesOpti();
    return 0;
}