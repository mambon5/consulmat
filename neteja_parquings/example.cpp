#include <iostream>
#include "SimplexCPP/Simplex.h"

using namespace std;

/*
Solve using the Simplex method the following problem:
Maximize 	Z = f(x,y) = 3x + 2y
subject to: 	2x + y ≤ 18
                2x + 3y ≤ 42
                3x + y ≤ 24
                x ≥ 0 , y ≥ 0
*/
int main()
{	
    // problem setup
    MATRIX problem = {
	LINE("w1",      { 2, 1, 1, 0, 0, 18 }),
	LINE("w2",      { 2, 3, 0, 1, 0, 42 }),
        LINE("w3",  { 3, 1, 0, 0, 1, 24 }),
	LINE("P",       {-3,-2, 0, 0, 0, 0 })
    };
		
    S_RESULTS result = Simplex::SolveEq(problem, 2); // where 2 is the total number of variables

    cout << result.GetValue("Pmax") << endl; // 33

     cout << "restriccio 1: " << result.GetValue("w1") << endl; // 33
     cout << "restriccio 2: " << result.GetValue("w2") << endl; // 33
     cout << "restriccio 3: " << result.GetValue("w3") << endl; // 33

    cout << " x01:" << result.GetValue("x1") << " x02:" << result.GetValue("x2") << endl;
   
    return 0;
}