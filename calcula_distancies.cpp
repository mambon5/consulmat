#include <iostream>
#include <string>
#include <curl/curl.h>
#include <json/json.h>
#include <unistd.h> // Per a sleep()
#include "textProcess.h"
#include <regex>
#include <thread>
#include <chrono>
#include <vector>
#include <regex>
// compilar usant
// g++ dates.cpp textProcess.cpp calcula_distancies.cpp -o calcul_dist -I/usr/include/jsoncpp -ljsoncpp -lcurl

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


size_t WriteCallback2(void* contents, size_t size, size_t nmemb, string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}



// Funció per obtenir el temps de viatge entre dues coordenades amb OSRM
double getTravelTime(const string& origin, const string& destination) {
    CURL* curl;
    CURLcode res;
    string readBuffer;

    // amb cotxe
    std::string url = "http://router.project-osrm.org/route/v1/driving/" + origin + ";" + destination + "?overview=false";

    // a peu
    // string url = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/" + origin + ";" + destination + "?overview=false";
    
    cout << url << endl;
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback2);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            cerr << "Error en la petició: " << curl_easy_strerror(res) << endl;
            return -1;
        } else {
            
            // cout <<"resposta osrm: " << endl << readBuffer << endl;

            // Analitzar la resposta JSON
            Json::CharReaderBuilder reader;
            Json::Value jsonData;
            string errors;

            istringstream stream(readBuffer);
            if (Json::parseFromStream(reader, stream, &jsonData, &errors)) {
                if (!jsonData["routes"].empty()) {
                    int duration = jsonData["routes"][0]["duration"].asInt();
                    cout << "Temps de viatge: " << duration / 60 << " minuts" << endl;
                    return duration / 60;
                } else {
                    cerr << "No s'han trobat rutes." << endl;
                    return -1;
                }
            } else {
                cerr << "Error en l'anàlisi del JSON: " << errors << endl;
                return -1;
            }
        }
        curl_easy_cleanup(curl);
    }
    return -2;
}


std::vector<int> extractTravelTimes_aux1(const std::string& html) {
    std::regex time_regex(R"((\d+) min\\\"]])"); // Coincideix amb "X min"]]
    std::regex hours_regex(R"(\"(\d+) h(?: y (\d+))?\\\"]\])"); // Coincideix amb "X h"] o "X h y Y min"
    
    std::vector<std::pair<size_t, int>> orderedTimes; // Guarda {posició, minuts}
    std::smatch match;
    std::string::const_iterator searchStart(html.cbegin());

    // Buscar "X min"]]
    while (std::regex_search(searchStart, html.cend(), match, time_regex)) {
        int minutes = std::stoi(match[1]);
        orderedTimes.push_back({match.position(0) + (searchStart - html.cbegin()), minutes});
        searchStart = match.suffix().first;
    }

    searchStart = html.cbegin(); // Reset per buscar hores

    // Buscar "X h"] i "X h y Y min"]]
    while (std::regex_search(searchStart, html.cend(), match, hours_regex)) {
        int minutes = std::stoi(match[1]) * 60; // Convertir hores a minuts
        if (match[2].matched) { 
            minutes += std::stoi(match[2]); // Afegir els minuts si existeixen
        }
        orderedTimes.push_back({match.position(0) + (searchStart - html.cbegin()), minutes});
        searchStart = match.suffix().first;
    }

    // Ordenar per posició en el text original
    std::sort(orderedTimes.begin(), orderedTimes.end());

    // Extreure només els minuts en ordre
    std::vector<int> travelTimes;
    for (const auto& t : orderedTimes) {
        travelTimes.push_back(t.second);
    }

    return travelTimes;
}

void superRegex(const string & html) {
    cout << "fent superregex" << endl;
    std::regex time_regex(R"(\[\[\[\d\],\d+,\[\d+,\\\"(\d+) min\\\"\]\],\[\[\d\],\d+,\[\d+,\\\"(\d+) h(?: y (\d+))?\\\"\]\],\[\[\d\],\d+,\[\d+,\\\"(\d+) h\\\"\]\],\[\[\d\],\d+,\[\d+,\\\"(\d+) h(?: y (\d+))?\\\"\]\]\])");
   

    std::smatch match;
    std::vector<int> travelTimes;

    if (std::regex_search(html, match, time_regex)) {
        for (size_t i = 1; i < match.size(); i++) {  // match[0] és tota la coincidència, els altres són els valors
            if (match[i].matched) {
                travelTimes.push_back(std::stoi(match[i].str()));
            }
        }
    }

    // Mostra els resultats trobats
    for (size_t i = 0; i < travelTimes.size(); ++i) {
        std::cout << "T" << (i + 1) << ": " << travelTimes[i] << std::endl;
    }

}

vector<int> extractTravelTimes(const std::string& html) {
    std::regex time_regex(R"((\d+) min\\\"]])"); // Coincideix amb "X min"]]
    std::regex hours_regex(R"(\"(\d+) h(?: y (\d+))?\"]\])"); // Coincideix amb "X h"] o "X h y Y"]]
    // std::regex time_regex(R"((\d+)\s*h(?:\s*y\s*(\d+))?\s*|\b(\d+)\s*min\b)");

    std::vector<int> times;
    std::smatch match;
    std::string::const_iterator searchStart(html.cbegin());

    cout << "comptant els cops que apareixen les expressiosn" << endl;
    while (std::regex_search(searchStart, html.cend(), match, time_regex)) {
        cout <<"mathc 1: " <<stoi(match[1]) << endl;
        times.push_back(std::stoi(match[1]));
        searchStart = match.suffix().first;
    }
     superRegex( html) ;

    int car_time = -1;
    int public_transport_time = -1;
    int walking_time = -1;
    int bici_time = -1;



    if (times.size() == 4) {
         // Agafem les 4 últimes aparicions
        car_time = times[times.size() - 4];
        public_transport_time = times[times.size() - 3];
        walking_time = times[times.size() - 2];
        bici_time = times[times.size() - 1];
    }
    else if (times.size() == 3) {
        // Agafem les 3 últimes aparicions
       car_time = times[times.size() - 3];
       walking_time = times[times.size() - 2];
       bici_time = times[times.size() - 1];
   }
   else {
    cout << "el codi font no mostra el temps només en minuts. Provant extracció avançada..."<< endl;
    return extractTravelTimes_aux1(html);
    
   }

   

    

    // std::cout << "Temps en cotxe: " << car_time << " min" << std::endl;
    // std::cout << "Temps en transport públic: " << public_transport_time << " min" << std::endl;
    // std::cout << "Temps a peu: " << walking_time << " min" << std::endl;
    // std::cout << "Temps en bici: " << bici_time << " min" << std::endl;

    return vector<int> {car_time, public_transport_time, walking_time, bici_time};
}


// void extractTravelTimes(const std::string& html) {
//     std::regex time_regex(R"((\d+)\s*h(?:\s*y\s*(\d+))?\s*|\b(\d+)\s*min\b)");
//     std::vector<int> times;
//     std::smatch match;
//     std::string::const_iterator searchStart(html.cbegin());

//     while (std::regex_search(searchStart, html.cend(), match, time_regex)) {
//         int total_minutes = 0;

//         try {
//             if (match[1].matched) {  // Si té hores
//                 total_minutes += std::stoi(match[1]) * 60;
//                 if (match[2].matched) {  // Si també té minuts
//                     total_minutes += std::stoi(match[2]);
//                 }
//             } else if (match[3].matched) {  // Si només té minuts
//                 total_minutes = std::stoi(match[3]);
//             }
//         } catch (const std::invalid_argument& e) {
//             std::cerr << "Error: No s'ha pogut convertir el temps!" << std::endl;
//             continue;
//         }

//         times.push_back(total_minutes);
//         searchStart = match.suffix().first;
//     }

//     if (times.size() < 4) {
//         std::cerr << "No s'han trobat prou dades!" << std::endl;
//         return;
//     }

//     int car_time = times[times.size() - 4];
//     int public_transport_time = times[times.size() - 3];
//     int walking_time = times[times.size() - 2];
//     int metro_time = times[times.size() - 1];

//     std::cout << "Temps en cotxe: " << car_time << " min" << std::endl;
//     std::cout << "Temps en transport públic: " << public_transport_time << " min" << std::endl;
//     std::cout << "Temps a peu: " << walking_time << " min" << std::endl;
//     std::cout << "Temps en metro: " << metro_time << " min" << std::endl;
// }


// Funció per obtenir el temps de viatge entre dues coordenades amb OSRM
double getTravelTimeGmaps(const string& origin, const string& destination) {
    CURL* curl;
    CURLcode res;
    string readBuffer;
    string coutGmaps = "output/GmapsDistance.out";

    // amb cotxe
    // string url = "http://router.project-osrm.org/routed-foot/route/v1/driving/" + origin + ";" + destination + "?overview=false";

    // a peu
    // string url = "https://www.google.es/maps/dir/'41.604169,2.288270'/'41.620692,2.292574'";
    string url = "https://www.google.es/maps/dir/'"+origin+"'/'"+destination+"'";
    // string url = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/" + origin + ";" + destination + "?overview=false";
    
    cout << url << endl;
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback2);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Afegeix un User-Agent per simular un navegador
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");

        // Permet redireccions (seguiment de 302)
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        
        res = curl_easy_perform(curl);
        // cout <<"resposta Gmaps: " << endl << readBuffer << endl;
        WriteToFileOver(readBuffer, coutGmaps);
        cout << "extracting travel times" << endl;
        vector<int> temps = extractTravelTimes(readBuffer);

        if (res != CURLE_OK) {
            cerr << "Error en la petició: " << curl_easy_strerror(res) << endl;
            return -1;
        } else {
            cout << "temps de viatge: " << endl;
            OutputVectorInt(temps);
        }
        curl_easy_cleanup(curl);
    }
    return -2;
}

vector<vector<double>> DistanceMatrix(const vector<vector<string>>& locations, bool symmetric=true) {
    int n = locations.size();
    vector<vector<double>> matrix(n, vector<double>(n, 0.0));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == j) continue; // La distància a si mateix és 0
            if(symmetric && i>j) {
                matrix[i][j] = matrix[j][i]; // no perdre temps tornant a calcular valors simètrics
                continue;
            }
            string origen = locations[i][2] + "," +  locations[i][3];
            string desti = locations[j][2] + "," + locations[j][3];

            cout << "punt1 (" + origen + ") punt2: (" + desti + ")" << endl;  
            
            matrix[i][j] = getTravelTimeGmaps(origen, desti); // Aquesta funció hauria d'omplir el resultat
            // Suposant que podem modificar getTravelTime perquè retorni el valor:
            // matrix[i][j] = getTravelTime(origin, destination);
        }
    }
    
    return matrix;
}

int main() {
    string inputfile="input/Comunidades_coords.csv";
    string outputDistances="output/Comunidades_distancies.csv";
    string outputPerdudes="output/Comunidades_dist_perdudes.csv";
    
    // vector<string> adreces = readCsv(fitxer);
    vector<vector<string>> coords = readCsvToMatrixFree(inputfile);// id, adreça, lat, lon

    string adreces_amb_coords= "";
    string adreces_perdudes= "";

    // buida els fitxers:
    WriteToFileOver("", outputDistances);
    WriteToFileOver("", outputPerdudes);

    
    int num_punts = 6;
    vector<vector<string>> sub_v(coords.begin(), coords.begin() + num_punts);
    Output2DVectorString(sub_v);

    // vector<vector<double>> dismat = DistanceMatrix(sub_v);

    // for(int i=0; i<num_punts; ++i) {
    //     for(int j=0; j<num_punts; ++j) {
    //         cout << "distancia de " + sub_v[i][0] + " a " + sub_v[j][0] +":" << endl;
    //         double time = getTravelTimeGmaps(sub_v[i][2]+","+sub_v[i][3],sub_v[j][2]+","+sub_v[j][3]);
    //     }        
    // }
            double time = getTravelTimeGmaps("41.364960,2.118542","41.606921,2.285211");

    // vector<vector<double>> matDistancies = DistanceMatrix(sub_v);
    // cout << "matriu de distàncies: " << endl;
    // Output2DVectorDouble(matDistancies); 

    

    return 0;
}
