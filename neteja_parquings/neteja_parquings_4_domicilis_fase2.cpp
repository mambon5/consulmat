#include <iostream>
#include "SimplexCPP/Simplex.h"
#include "src/textProcess.h"


using namespace std;

// compile by the command: 
// g++ SimplexCPP/include/fraction.cpp  src/dates.cpp src/textProcess.cpp neteja_parquings_4_domicilis_eq_com2_ineq.cpp -o neteja_4_parquings


/*
Solve using the Simplex method the following problem:
Maximize 	Z = f(x,y) = 3x + 2y
subject to: 	2x + y ≤ 18
                2x + 3y ≤ 42
                3x + y ≤ 24
                x ≥ 0 , y ≥ 0
*/

// distancies de parquing "i" a parquing "j". dij.
vector<vector<int>> d = { {5, 10, 2, 10}, {5,5,7,15}, {10, 5, 15, 17}, 
                             {2, 7, 15, 9}, {10, 15, 17, 9}} ; 

// temps en netejar el pàrquing "i", ti en minuts:
vector<int> t = {30, 120, 180, 60, 240};



int main()
{	
    Output2DVectorInt(d);
    OutputVectorInt(t);
    // problem setup
    // tenim 6 equacions i 7 inequacions per definir el problema. 
    // Un conjunt de 20 variables booleans xij, i 7 variables d'amortiguament per les inequacions.
    MATRIX problem = {
        // que sumin tots els temps de viatge pel seu temps de neteja, menys de 6h30'
	LINE("w1", { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3],
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                 480 // valor de la equació o inequació 
                 }),
                // que sumin tots els temps de viatge pel seu temps de neteja, més de 5h'
	LINE("w2", { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3],
                 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                180 // valor de la equació o inequació 
                }),
    
    // es surt 1 cop de la base (parquing 0)
    LINE("w3", { 1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0, 
                0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),

    LINE("w4", {1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0, 
                0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                 1 }),
     // de cada pàrquing es surt com a molt 1 cop (parking 0)
    LINE("w5", { 1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0, 
                0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),
    //  (parking 1)
    LINE("w6", { 0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0, 
                0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),
    //  (parking 2)
    LINE("w7", { 0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0, 
                0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),
    //  (parking 3)
    LINE("w8", { 0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0, 
                0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),
    //  (parking 4)
    LINE("w9", { 0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                1 }),

    // es surt la mateixa quantitat de cops que s'entra en cada pàrquing
        //  (parking 0)
    LINE("w10", { 1, 1, 1, 1, 
                -1, 0, 0,0,
                -1, 0, 0,0,
                -1, 0, 0,0,
                -1, 0, 0,0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                0 }),
     LINE("w11", {  1, 1, 1, 1, 
                -1, 0, 0,0,
                -1, 0, 0,0,
                -1, 0, 0,0,
                -1, 0, 0,0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,  // variables d'amortiguament
                0 }),
        //  (parking 1)
    LINE("w12", {-1,0, 0, 0, 
                 1, 1, 1, 1, 
                 0,-1, 0,0,
                 0,-1, 0,0,
                 0,-1, 0,0, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                0 }),
    LINE("w13", { -1,0, 0, 0, 
                 1, 1, 1, 1, 
                 0,-1, 0,0,
                 0,-1, 0,0,
                 0,-1, 0,0, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, // variables d'amortiguament
                0 }),
        //  (parking 2)
     LINE("w14", {0,-1, 0, 0, 
                  0,-1, 0,0,
                  1, 1, 1, 1, 
                  0, 0,-1,0,
                  0, 0,-1,0, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, // variables d'amortiguament
                0 }),
    LINE("w15", {0,-1, 0, 0, 
                  0,-1, 0,0,
                  1, 1, 1, 1, 
                  0, 0,-1,0,
                  0, 0,-1,0,  
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, // variables d'amortiguament
                0 }),
        //  (parking 3)
     LINE("w16",{0, 0,-1, 0,  
                 0, 0,-1, 0, 
                 0, 0,-1, 0, 
                 1, 1, 1, 1, 
                 0, 0, 0,-1, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,// variables d'amortiguament
                0 }),
    LINE("w17", { 0, 0,-1, 0,  
                 0, 0,-1, 0, 
                 0, 0,-1, 0, 
                 1, 1, 1, 1, 
                 0, 0, 0,-1,  
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, // variables d'amortiguament
                0 }),
        //  (parking 4)
     LINE("w18", {0, 0, 0,-1,  
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 1, 1, 1, 1, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,// variables d'amortiguament
                0 }),
    LINE("w19", { 0, 0, 0,-1,  
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 1, 1, 1, 1, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1,// variables d'amortiguament
                0 }),

   
	LINE("P", { d[0][0], d[0][1], d[0][2], d[0][3], 
                d[1][0], d[1][1], d[1][2], d[1][3],
                d[2][0], d[2][1], d[2][2], d[2][3], 
                d[3][0], d[3][1], d[3][2], d[3][3],
                d[4][0], d[4][1], d[4][2], d[4][3],
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // variables d'amortiguament 
                0 // constant
                })
    };
		
    S_RESULTS result = Simplex::SolveEq(problem, 20, true); // where 2 is the total number of variables

    cout << " x01:" << result.GetValue("x1") << " x02:" << result.GetValue("x2") << " x03:" <<
    result.GetValue("x3") << " x04:" << result.GetValue("x4") << endl;
    cout << " x10:" <<
    result.GetValue("x5") << " x12:" << result.GetValue("x6") << 
     " x13:" << result.GetValue("x7") << " x14:" <<
    result.GetValue("x8") << endl;
    cout << " x20:" << result.GetValue("x9") <<" x21:" <<
    result.GetValue("x10") << " x23:" << result.GetValue("x11") <<
     " x24:" << result.GetValue("x12") << endl;
     cout << " x30:" <<
    result.GetValue("x13") << " x31:" << result.GetValue("x14") <<" x32:" <<
    result.GetValue("x15") << " x34:" <<  result.GetValue("x16") << endl;
    cout <<      " x40:" << result.GetValue("x17") << " x41:" <<
    result.GetValue("x18") << " x42:" << result.GetValue("x19") <<" x43:" <<
    result.GetValue("x20") <<  endl;

    cout << "valor funció objectiu: " << result.GetValue("Pmax") << endl; // 33

    cout << "rest1: " << result.GetValue("w1") << endl; // 33
    cout << "rest2: " << result.GetValue("w2") << endl; // 33
    cout << "rest3: " << result.GetValue("w3") << endl; // 33
    cout << "rest4: " << result.GetValue("w4") << endl; // 33
    cout << "rest5: " << result.GetValue("w5") << endl; // 33
    cout << "rest6: " << result.GetValue("w6") << endl; // 33
    cout << "rest7: " << result.GetValue("w7") << endl; // 33
    cout << "rest8: " << result.GetValue("w8") << endl; // 33
    cout << "rest9: " << result.GetValue("w9") << endl; // 33
    cout << "rest10: " << result.GetValue("w10") << endl; // 33
    cout << "rest11: " << result.GetValue("w11") << endl; // 33
    cout << "rest12: " << result.GetValue("w12") << endl; // 33
    cout << "rest13: " << result.GetValue("w13") << endl; // 33
    cout << "rest14: " << result.GetValue("w14") << endl; // 33
    cout << "rest15: " << result.GetValue("w15") << endl; // 33
    cout << "rest16: " << result.GetValue("w16") << endl; // 33
    cout << "rest17: " << result.GetValue("w17") << endl; // 33
    cout << "rest18: " << result.GetValue("w18") << endl; // 33
    cout << "rest19: " << result.GetValue("w19") << endl; // 33

    cout << "matriu d:" << endl;
    Output2DVectorInt(d);

    cout << "hola" << endl;

    return 0;
}

