#include <iostream>
#include <fstream>
#include <vector>
#include <string>


using namespace std;


vector<int> flattenMatrix(const vector<vector<int>>& matrix) {
    vector<int> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}

// Funció recursiva per aplanar un vector n-dimensional
template <typename T>
void flattenHelper(const T& matrix, vector<int>& result) {
    result.push_back(matrix);
}

// Especialització per a vectors
template <typename T>
void flattenHelper(const vector<T>& matrix, vector<int>& result) {
    for (const auto& subMatrix : matrix) {
        flattenHelper(subMatrix, result);
    }
}

// Funció principal per aplanar qualsevol vector n-dimensional
template <typename T>
vector<int> flattenMatrix_ndim(const T& matrix) {
    vector<int> result;
    flattenHelper(matrix, result);
    return result;
}

vector<string> flattenMatrixString(const vector<vector<string>>& matrix) {
    vector<string> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}