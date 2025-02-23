#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <ctime>
#include <chrono>
#include <thread>
#include <cstring>
#include <dirent.h>
#include <sys/types.h>
#include <iomanip>
#include <curl/curl.h>
#include "dates.h"

using namespace std;

string PrintNumberWithXDecimalsDoub(const double& number, const int& precision);
bool compareStrings(const std::string& str1, const std::string& str2);
void sortarray(vector<std::string>& arrayDeStrings);

class sort_indices
{
    // sorts the indices instead of the array!
    // how to use it:
    // int arr[5]={4,1,3,6,2}
    // string arr1[5]={"a1","b1","c1","d1","e1"};
    // int indices[5]={0,1,2,3,4};
    // arr[indices[0]]
    // std::sort(indices, indices+5, sort_indices(arr));
    //
   private:
     int* mparr;
   public:
     sort_indices(int* parr) : mparr(parr) {}
     bool operator()(int i, int j) const { return mparr[i]<mparr[j]; }
};

string removeNulls(const std::string& input);
void removeQuotes(std::vector<std::string>& arr);
string urlencode(const std::string &value);
void removeInvalidStrings(std::vector<std::string>& arr);
void printCharCodes(const string& str);
std::string removeTextAfterParenthesis(const std::string& input);
string trim(const string& str);

string DownloadWebBody(const string& url);
size_t WriteCallback(void* ptr, size_t size, size_t nmemb, string* userdata);
std::string DownloadWebContent(const std::string& url);
std::string getTableStocks(const std::string& body);
std::string DirectWebContent(std::string& searchGroup, std::string B, std::string C);
bool StringInVector(const std::string& ticker, const vector<std::string>& tickers);

void LenghtOfVector(const vector<std::string>& tickers);
int LenghtOfVectorStr(const vector<string>& tickers);
int LenghtOfMatStr(const vector<vector<string>>& tickers);
int LenghtOfVectorInt(const vector<int>& tickers);
int LenghtOfVectorDoub(const vector<double>& tickers);

void OutputVector(const vector<std::string>& tickers, string sep="\n");
void OutputVectorInt(const vector<int>& tickers);
void OutputVectorDouble(const vector<double>& tickers);
void Output2DVectorDouble(const vector<vector<double>>& matrix);
void Output2DVectorString( const vector<vector<string>>& matrix);
void Output2Dvector_custom1(const vector<vector<double>>& matrix, const vector<string>& strings);
void Output2Dvector_firstFew(const vector<vector<double>>& matrix, const vector<string>& strings, int show=5);

void Write2Dvector_firstFew(const vector<vector<double>>& matrix, const vector<string>& strings, const std::string& outputFile, int show=5);
void WriteToFileSimple(const std::string& output, const std::string& outputFile, bool printall=false);
void WriteToFileOver(const std::string& output, const std::string& outputFile, bool printall=false);
void WriteToFile(const vector<std::string>& tickers, const std::string& outputFile, bool showVector=false);

string vectorDoubleToString(const vector<double>& vector);
string ExtractDateFromFile(const string& filename);
bool TodayFileExists(const string& dirname, const string& filenameSuffix);
void DeleteOlderFiles(const string& dirname, const string& filenameSuffix, const int& daysOld, bool printAll=true);

vector<std::string> getLastSearchGroup();
int getLastFileNumber();

vector<double> extractNthColumnFromString(const string& text, const int& columna);
vector<string> extractNthColumnFromCsvString(const string& filename, const int& columna, const char sep = ',', bool deleteFirstRow=false);
vector<vector<string>> readCsvToMatrix(const string& filename, const int& columns);
vector<vector<string>> readCsvToMatrixFree(const string& filename, const int& inici);
string readFile(const std::string& filename);
vector<std::string> readCsv(const std::string& filename);
string GetFirstLineOfFile(const std::string& inputFile, bool printall=false);


vector<std::string> readPartialCsvFromCertainLine(const std::string& filename, 
                const int& elems, const string firstTick, bool printOutput=false) ;

vector<std::string> readPartialCsv(const std::string& filename, const int& elems, bool printOutput=false) ;

vector<string> StringToStringArray(const std::string& csvText);

string FindArrayFromJson(const std::string& json, const string& label, bool printOutput=false) ;

vector<string> JsonToStringArray(const std::string& json, const string& label, bool printOutput=false);

vector<std::string> CsvFilterDuplicates(const std::string& filename);

string replaceChars(string text, char const & oldChar, char const & newChar, bool elimina=false);

bool file_exists(const string fileName);
