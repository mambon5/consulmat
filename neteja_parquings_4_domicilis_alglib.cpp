#include <iostream>
#include <libalglib/stdafx.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <libalglib/optimization.h>
#include "src/textProcess.h"



// compile by the command: 
// g++  src/dates.cpp src/textProcess.cpp neteja_parquings_4_domicilis_alglib.cpp -o neteja_4_parquings_alglib -lalglib


using namespace alglib;



string convertVecToALGLIBFormat(const vector<int>& vec) {
    stringstream ss;
    ss << "[";
    
    for (size_t i = 0; i < vec.size(); ++i) {
        ss << vec[i];
        if (i != vec.size() - 1) {
            ss << ",";
        }
    }
    
    ss << "]";
    return ss.str();
}

string convertMatToALGLIBFormat(const vector<vector<int>>& mat) {
    stringstream ss;
    ss << "[";
    
    for (size_t i = 0; i < mat.size(); ++i) {
        ss << convertVecToALGLIBFormat(mat[i]);
        if (i != mat.size() - 1) {
            ss << ",";
        }
    }
    
    ss << "]";
    return ss.str();
}

vector<int> flattenMatrix(const vector<vector<int>>& matrix) {
    vector<int> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}


void printArrayInRows(const real_1d_array& x, int num_per_row) {
    for (int i = 0; i < x.length(); ++i) {
        printf("%.3f", x[i]);
        if ((i + 1) % num_per_row == 0) {
            printf("\n");
        } else {
            printf(", ");
        }
    }
    printf("\n");
}


void fesOpti()
{
    try
    {
        //
        // This example demonstrates how to minimize
        //
        //     F(x0,x1) = -0.1*x0 - x1
        //
        // subject to box constraints
        //
        //     -1 <= x0,x1 <= +1 
        //
        // and general linear constraints
        //
        //     x0 - x1 >= -1
        //     x0 + x1 <=  1
        //
        // We use dual simplex solver provided by ALGLIB for this task. Box
        // constraints are specified by means of constraint vectors bndl and
        // bndu (we have bndl<=x<=bndu). General linear constraints are
        // specified as AL<=A*x<=AU, with AL/AU being 2x1 vectors and A being
        // 2x2 matrix.
        //
        // NOTE: some/all components of AL/AU can be +-INF, same applies to
        //       bndl/bndu. You can also have AL[I]=AU[i] (as well as
        //       BndL[i]=BndU[i]).
        //

    // distancies de parquing "i" a parquing "j". dij.
    vector<vector<int>> d = { {5, 10, 2, 10}, {5,5,7,15}, {10, 5, 15, 17}, 
                                {2, 7, 15, 9}, {10, 15, 17, 9}} ; 
    
     vector<int> dist = flattenMatrix(d);

    cout << "vector distàncies:  " << endl;
    OutputVectorInt(dist);

    // temps en netejar el pàrquing "i", ti en minuts:
    vector<int> t = {30, 120, 180, 60, 240};

    vector<int> res1 = { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3]
                 };
                // que sumin tots els temps de viatge pel seu temps de neteja, més de 5h'
	vector<int> res2 =  { d[0][0]+t[1], d[0][1]+t[2], d[0][2]+t[3], d[0][3]+t[4], 
                d[1][0]+t[0], d[1][1]+t[2], d[1][2]+t[3], d[1][3]+t[4],
                d[2][0]+t[0],d[2][1]+t[1], d[2][2]+t[3], d[2][3]+t[4], 
                d[3][0]+t[0],d[3][1]+t[1], d[3][2]+t[2], d[3][3]+t[4],
                d[4][0]+t[0],d[4][1]+t[1], d[4][2]+t[2], d[4][3]+t[3]
                };
    
    // es surt 1 cop de la base (parquing 0)
    vector<int> res3 =  { 
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0
                };

     // de cada pàrquing es surt com a molt 1 cop 
     //  (parking 0)
    vector<int> res4 =  { 
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0
                };
    //  (parking 1)
    vector<int> res5 =  { 
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0
                 };
    //  (parking 2)
    vector<int> res6 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0,
                0, 0, 0,0
                };
    //  (parking 3)
    vector<int> res7 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1, 
                0, 0, 0,0
                };
    //  (parking 4)
    vector<int> res8 =  { 
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                0, 0, 0,0,
                1, 1, 1, 1
                };

    // es surt la mateixa quantitat de cops que s'entra en cada pàrquing
        //  (parking 0)
   vector<int> res9 =  { 
                1, 1, 1, 1, 
                 -1, 0, 0,0,
                 -1, 0, 0,0,
                 -1, 0, 0,0,
                 -1, 0, 0,0
                 };
        //  (parking 1)
    vector<int> res10 =  {
                -1, 0, 0, 0, 
                  1, 1, 1, 1, 
                  0,-1, 0,0,
                  0,-1, 0,0,
                  0,-1, 0,0
                   };
   
        //  (parking 2)
     vector<int> res11 =  { 
                0,-1, 0, 0, 
                  0,-1, 0,0,
                  1, 1, 1, 1, 
                  0, 0,-1,0,
                  0, 0,-1,0 };
   
        //  (parking 3)
     vector<int> res12 =  {
                0, 0,-1, 0,  
                 0, 0,-1, 0, 
                 0, 0,-1, 0, 
                 1, 1, 1, 1, 
                 0, 0, 0,-1};
   
        //  (parking 4)
     vector<int> res13 =  {
                0, 0, 0,-1,  
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 0, 0, 0, -1, 
                 1, 1, 1, 1};
   

   

    
		

        vector<vector<int>> res = {res1,res2,res3,res4,res5,res6,res7,res8,
        res9,res10,res11,res12,res13};
        real_2d_array a =  convertMatToALGLIBFormat(res).c_str();
        real_1d_array al = "[-inf,180,1,0,0,0,0,0,0,0,0,0,0]";
        real_1d_array au = "[480,+inf,1,1,1,1,1,1,0,0,0,0,0]";
        real_1d_array c = convertVecToALGLIBFormat(dist).c_str();;
        real_1d_array s =       "[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]"; // escala de cada variable
        real_1d_array bndl =    "[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]";
        real_1d_array bndu =    "[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]";
        real_1d_array x;
        minlpstate state;
        minlpreport rep;

        minlpcreate(20, state);

        //
        // Set cost vector, box constraints, general linear constraints.
        //
        // Box constraints can be set in one call to minlpsetbc() or minlpsetbcall()
        // (latter sets same constraints for all variables and accepts two scalars
        // instead of two vectors).
        //
        // General linear constraints can be specified in several ways:
        // * minlpsetlc2dense() - accepts dense 2D array as input; sometimes this
        //   approach is more convenient, although less memory-efficient.
        // * minlpsetlc2() - accepts sparse matrix as input
        // * minlpaddlc2dense() - appends one row to the current set of constraints;
        //   row being appended is specified as dense vector
        // * minlpaddlc2() - appends one row to the current set of constraints;
        //   row being appended is specified as sparse set of elements
        // Independently from specific function being used, LP solver uses sparse
        // storage format for internal representation of constraints.
        //
        minlpsetcost(state, c);
        minlpsetbc(state, bndl, bndu);
        minlpsetlc2dense(state, a, al, au, 13);

        //
        // Set scale of the parameters.
        //
        // It is strongly recommended that you set scale of your variables.
        // Knowing their scales is essential for evaluation of stopping criteria
        // and for preconditioning of the algorithm steps.
        // You can find more information on scaling at http://www.alglib.net/optimization/scaling.php
        //
        minlpsetscale(state, s);

        //
        // Solve with the sparse IPM.
        //
        // Commercial ALGLIB can parallelize sparse Cholesky factorization which is the
        // most time-consuming part of the algorithm. See the ALGLIB Reference Manual for
        // more information on how to activate parallelism support.
        //
        minlpsetalgoipm(state);
        minlpoptimize(state);
        minlpresults(state, x, rep);
        // printf("%s\n", x.tostring(3).c_str()); // EXPECTED: [0,1]
          printArrayInRows(x, 4);
         printf("%s\n", au.tostring(3).c_str()); // EXPECTED: [0,1]
    }
    catch(alglib::ap_error alglib_exception)
    {
        printf("ALGLIB exception with message '%s'\n", alglib_exception.msg.c_str());
        
    }
}

int main(int argc, char **argv) {
   
   
     fesOpti();
    return 0;
}