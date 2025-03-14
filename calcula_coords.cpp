#include <iostream>
#include <string>
#include <curl/curl.h>
#include <json/json.h>
#include <unistd.h> // Per a sleep()
#include "textProcess.h"
#include <regex>
#include <thread>
#include <chrono>
// compilar usant
// g++ dates.cpp textProcess.cpp calcula_coords.cpp -o calcul_coord -I/usr/include/jsoncpp -ljsoncpp -lcurl

using namespace std;

// extreu les coordenades a partir de la URL de google maps:
string extractCoordinates(const string& url) {
    regex regexPattern(R"(@([-+]?\d*\.\d+),([-+]?\d*\.\d+))");
    smatch match;

    if (regex_search(url, match, regexPattern) && match.size() >= 3) {
        double latitude = stod(match[1].str());
        double longitude = stod(match[2].str());
        return  to_string(latitude) +"," + to_string(longitude) ;
    } else {
        cout << "ERROR en extractCoordinates(): No s'han trobat coordenades a la URL." << endl;
        return "";
    };
    
}

string obtenirGoogleMapsURL(const string& adreca) {
    CURL* curl;
    CURLcode res;
    string readBuffer;
    string outFile = "output/gmapsout.out" ;
    
    curl = curl_easy_init();
    if (curl) {
        string url = "https://www.google.com/maps/search/?q=" + urlencode(adreca);
        // string url = "https://www.google.com/search?q=" + urlencode(adreca);
        
        cout << "url google usada: " << url << endl;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Afegeix un User-Agent per simular un navegador
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");

        // Permet redireccions (seguiment de 302)
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        // resposta de google maps;
        WriteToFileSimple(readBuffer,outFile);
        

        if (res != CURLE_OK) {
            cerr << "Error HTTP: " << curl_easy_strerror(res) << endl;
            return "";
        }
    }

    // Buscar la primera URL de Google Maps dins l’HTML
    regex mapsRegex(R"(https:\/\/www\.google\.com\/maps\/preview\/place\/[^"]+)");
    smatch match;
    if (regex_search(readBuffer, match, mapsRegex)) {
        // mostra la resposta de la curl requests, si no es poden trobar les coordenades
        if(extractCoordinates(match.str(0)).empty()) {
            cout << "response buffer: " << endl;
            cout << readBuffer << endl;
        }
        return match.str(0); // Retorna la primera coincidència
    }

    return "No trobada";
}

vector<string> extractAddresses(const vector<vector<string>>& matrix) {
    vector<string> addresses;
    
    for (const auto& row : matrix) {
        if (row.size() >= 5) { // Comprovar que té prou columnes
            // string fullAddress = trim(row[5]) + " " + trim(row[6]) + " " + trim(row[2]) + 
                                " " + trim(row[3])  + " " + trim(row[4]); 
              string fullAddress = trim(row[4]) + " " + trim(row[2]) + " " + trim(row[1]) + 
                                " " + trim(row[3]); 
            addresses.push_back(fullAddress);
        }
    }
    return addresses;
}

vector<string> extractIDs(const vector<vector<string>>& matrix) {
    vector<string> address_ids;
    
    for (const auto& row : matrix) {
        if (row.size() >= 5) { // Comprovar que té prou columnes
            string id = trim(row[0]) ;
            address_ids.push_back(id);
        }
    }
    return address_ids;
}

size_t WriteCallback2(void* contents, size_t size, size_t nmemb, string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

// Funció per obtenir coordenades a partir d'una adreça mitjançant Google Maps sense API key
string getCoordinates(const string& adreca) {
    string mapsURL = obtenirGoogleMapsURL(adreca);
    return  extractCoordinates(mapsURL);
}

int main() {
   
    string inputfile="input/Comunidades_11_03_2025.csv";
    string outputCoords="output/Comunidades_coords.csv";
    string outputPerdudes="output/Comunidades_perdudes.csv";
    
    // vector<string> adreces = readCsv(fitxer);
    vector<vector<string>> adreces2 = readCsvToMatrixFree(inputfile, 1);


    vector<string> addresses = extractAddresses(adreces2);
    vector<string> ids = extractIDs(adreces2);
    

    string adreces_amb_coords= "";
    string adreces_perdudes= "";

    // buida els fitxers:
    WriteToFileOver("", outputCoords);
    WriteToFileOver("", outputPerdudes);

    int i = 0;
    for(string adreça : addresses) {
       
        if(i <0) break; // defineix si volem que llegeixi un nombre maxim d'adreces 
        // Obtenir coordenades per les adreces
        this_thread::sleep_for(chrono::milliseconds(500));  
        int retries = 3;  // Nombre màxim d'intents
        string originCoords;
        string adreça_orig = adreça;

        while (retries > 0) { //si no es troba l'adreça, reintenta
            originCoords = getCoordinates(adreça);

            if (!originCoords.empty()) {                
                adreces_amb_coords = ids[i] + ", " + adreça + "," + originCoords;
                WriteToFileSimple(adreces_amb_coords, outputCoords);
                break;  // Si s'han trobat les coordenades, sortim del bucle
            } else {
                cout << "No s'han trobat coordenades per: " << adreça << ". Reintentant..." << endl;
                if(retries == 3) {
                    adreça = "Carrer de " + adreça; // afegeix la C per buscar la adreça millor.
                }
                
                else {
                    this_thread::sleep_for(chrono::seconds(10));    // Espera 10 segons abans de reintentar
                }
                
                retries--;
            }
        }

        if (originCoords.empty()) {
            WriteToFileSimple(ids[i]  + ", " + adreça_orig, outputPerdudes);
        }
        

        cout << adreça + "," + originCoords << endl;
        ++i;
    }

    

    return 0;
}
