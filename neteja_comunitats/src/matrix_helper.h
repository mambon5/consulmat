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
void flattenHelper_int(const T& matrix, vector<int>& result) {
    result.push_back(matrix);
}

// Especialització per a vectors
template <typename T>
void flattenHelper_int(const vector<T>& matrix, vector<int>& result) {
    for (const auto& subMatrix : matrix) {
        flattenHelper_int(subMatrix, result);
    }
}

// Funció principal per aplanar qualsevol vector n-dimensional
template <typename T>
vector<int> flattenMatrix_ndim_int(const T& matrix) {
    vector<int> result;
    flattenHelper_int(matrix, result);
    return result;
}

// Funció recursiva per aplanar un vector n-dimensional
template <typename T>
void flattenHelper_str(const T& matrix, vector<string>& result) {
    result.push_back(matrix);
}

// Especialització per a vectors
template <typename T>
void flattenHelper_str(const vector<T>& matrix, vector<string>& result) {
    for (const auto& subMatrix : matrix) {
        flattenHelper_str(subMatrix, result);
    }
}

// Funció principal per aplanar qualsevol vector n-dimensional
template <typename T>
vector<string> flattenMatrix_ndim_str(const T& matrix) {
    vector<string> result;
    flattenHelper_str(matrix, result);
    return result;
}

vector<string> flattenMatrixString(const vector<vector<string>>& matrix) {
    vector<string> result;

    for (const auto& row : matrix) {
        result.insert(result.end(), row.begin(), row.end());
    }

    return result;
}

vector<vector<int>> submatriu_superior_esquerra(const vector<vector<int>>& matriu, int m) {
    int n = matriu.size();

    if (m > n) {
        throw invalid_argument("m ha de ser menor o igual a n");
    }

    vector<vector<int>> submatriu(m, vector<int>(m));

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < m; ++j) {
            submatriu[i][j] = matriu[i][j];
        }
    }

    return submatriu;
}


std::vector<int> suma_vectors(const std::vector<int>& a, const std::vector<int>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Els vectors han de tenir la mateixa mida.");
    }

    std::vector<int> resultat(a.size());

    for (size_t i = 0; i < a.size(); ++i) {
        resultat[i] = a[i] + b[i];
    }

    return resultat;
}

void llegir_dos_vectors(const string& nom_fitxer, vector<int>& col1, vector<int>& col2) {
    ifstream fitxer(nom_fitxer);
    if (!fitxer.is_open()) {
        throw runtime_error("No s'ha pogut obrir el fitxer");
    }

    string linia;
    while (getline(fitxer, linia)) {
        stringstream ss(linia);
        int val1, val2;
        if (ss >> val1 >> val2) {
            col1.push_back(val1);
            col2.push_back(val2);
        }
    }

    fitxer.close();
}