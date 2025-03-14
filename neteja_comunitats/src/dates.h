#pragma once //fa que es compili només 1 vegada
#include <iostream> 
#include <chrono>


using namespace std; 
// C++ program two find number of  
// days between two given dates 

// es fan les definicions en el fitxer .h que incloem múltiples cops,i la declaració en un únic fitxer dates.cpp que s'inclou al compilar,
// per evitar errors deredefinició. 

extern const int monthDays[12];

// Declaració de les funcions
// A date has day 'd', month 'm' and year 'y' 
struct Date { 
    int d, m, y; 
};

int countLeapYears(Date d);
long int comptaDies(Date date);
int calcularDiesEntreDates(Date dt1, Date dt2);
int DiesEntreDates(const std::string & date1, const std::string & date2);
std::string getCurrentDate();
std::string yesterday();
string today();
