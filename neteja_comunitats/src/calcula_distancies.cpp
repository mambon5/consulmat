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

// fitxer d'accés global
string currentDate = getCurrentDate();
// string currentDate = "2025-03-16"; // borrar aquesta linia per seguretat.
string inputfile="../input/Comunidades_coords.csv";
string outputDistCotxe="../output/DistCotxe_"+currentDate+".csv";
string outputDistMetro="../output/DistMetro_"+currentDate+".csv";
string outputDistPeu="../output/DistPeu_"+currentDate+".csv";
string outputDistBici="../output/DistBici_"+currentDate+".csv";




size_t WriteCallback2(void* contents, size_t size, size_t nmemb, string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}




std::vector<int> extractTravelTimes_aux1(const std::string& html, bool debug = false) {
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

    if(debug) {
        cout << "extractTravelTimes_aux1(): travel times: " << endl;
        OutputVectorInt(travelTimes);
    }
    // torna els últims 4 com a molt
    int extres = travelTimes.size() - 4;
    if(extres > 0) {
         vector<int> v(travelTimes.begin()+extres, travelTimes.end());
         return v;
    }

    return travelTimes;
}

void superRegex(const string & html, bool print = false) {
    // cout << "fent superregex" << endl;
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
    if(print) {
        for (size_t i = 0; i < travelTimes.size(); ++i) {
            std::cout << "T" << (i + 1) << ": " << travelTimes[i] << std::endl;
        }
    }
   

}

vector<int> extractTravelTimes(const std::string& html, bool debug=false) {
    std::regex time_regex(R"((\d+) min\\\"]])"); // Coincideix amb "X min"]]
    std::regex hours_regex(R"(\"(\d+) h(?: y (\d+))?\"]\])"); // Coincideix amb "X h"] o "X h y Y"]]
    // std::regex time_regex(R"((\d+)\s*h(?:\s*y\s*(\d+))?\s*|\b(\d+)\s*min\b)");

    std::vector<int> times;
    std::smatch match;
    std::string::const_iterator searchStart(html.cbegin());

    // cout << "comptant els cops que apareixen les expressiosn" << endl;
    while (std::regex_search(searchStart, html.cend(), match, time_regex)) {
        // cout <<"mathc 1: " <<stoi(match[1]) << endl;
        times.push_back(std::stoi(match[1]));
        searchStart = match.suffix().first;
    }
     superRegex( html) ;

    int car_time = -1;
    int public_transport_time = -1;
    int walking_time = -1;
    int bici_time = -1;



//     if (times.size() == 4) {
//          // Agafem les 4 últimes aparicions
//         car_time = times[times.size() - 4];
//         public_transport_time = times[times.size() - 3];
//         walking_time = times[times.size() - 2];
//         bici_time = times[times.size() - 1];
//     }
//     else if (times.size() == 3) {
//         // Agafem les 3 últimes aparicions
//        car_time = times[times.size() - 3];
//        walking_time = times[times.size() - 2];
//        bici_time = times[times.size() - 1];
//    }
//    else {
    // cout << "el codi font no mostra el temps només en minuts. Provant extracció avançada..."<< endl;
    vector<int> times2= extractTravelTimes_aux1(html, debug);
    if(times2.size() == 3) {
        car_time = times2[0];
        walking_time = times2[1];
        bici_time= times2[2];
    }
    else {
        car_time = times2[0];
        public_transport_time = times2[1];
        walking_time = times2[2];
        bici_time= times2[3];
    }
    
//    }

   

    
    if(debug) {
        std::cout << "Temps en cotxe: " << car_time << " min" << std::endl;
        std::cout << "Temps en transport públic: " << public_transport_time << " min" << std::endl;
        std::cout << "Temps a peu: " << walking_time << " min" << std::endl;
        std::cout << "Temps en bici: " << bici_time << " min" << std::endl;    

    }
  
    return vector<int> {car_time, public_transport_time, walking_time, bici_time};
}

// Funció per obtenir el temps de viatge entre dues coordenades amb OSRM
vector<int> getTravelTimeGmaps(const string& origin, const string& destination, 
                                bool debug = false) {
    CURL* curl;
    CURLcode res;
    string readBuffer;
    string coutGmaps = "../output/GmapsDistance.out";
    vector<int> temps(4,-1);
    // amb cotxe
    // string url = "http://router.project-osrm.org/routed-foot/route/v1/driving/" + origin + ";" + destination + "?overview=false";

    // a peu
    // string url = "https://www.google.es/maps/dir/'41.604169,2.288270'/'41.620692,2.292574'";
    string url = "https://www.google.es/maps/dir/'"+origin+"'/'"+destination+"'";
    // string url = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/" + origin + ";" + destination + "?overview=false";
    
    if(debug) cout << url << endl;
    curl = curl_easy_init();
    if (curl) {

       


        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback2);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Afegeix un User-Agent per simular un navegador
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");
        // curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0");
        // curl_easy_setopt(curl, CURLOPT_REFERER, "https://www.google.com/");

        // Permet redireccions (seguiment de 302)
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        
        res = curl_easy_perform(curl);
        // cout <<"resposta Gmaps: " << endl << readBuffer << endl;
        // WriteToFileOver(readBuffer, coutGmaps);
        cout << "extracting travel times" << endl;
        temps = extractTravelTimes(readBuffer, debug);

        if (res != CURLE_OK) {
            cerr << "Error en la petició: " << curl_easy_strerror(res) << endl;
            
        } else if(debug){
            cout << "temps de viatge: " << endl;
            OutputVectorInt(temps);
        }
        curl_easy_cleanup(curl);
    }
    return temps;
}

void DistanceMatrixes(vector<vector<int>>& cotxe, vector<vector<int>>& metro, 
    vector<vector<int>>& peu, vector<vector<int>>& bici,
    const vector<vector<string>>& locations, string origIni, string destIni, bool symmetric=true, bool debug = false) {
    int n = locations.size();
    
    // vector<vector<int>> cotxe(n, vector<int>(n, 0.0)); // matriu distancia temps en cotxe
    // vector<vector<int>> metro(n, vector<int>(n, 0.0));// matriu distancia temps en metrobus
    // vector<vector<int>> peu(n, vector<int>(n, 0.0));
    // vector<vector<int>> bici(n, vector<int>(n, 0.0));
    int i0 = 0;
    int j0 = 0;
    
    if(origIni != "" && destIni != "") {
        i0 = stoi(origIni); // origIni es la comunitat 1 final calculada, i la latra la comunitat 2 ultima calculada
        j0 = stoi(destIni);
        if(j0 == locations.size()) { // si hem de canvair ara la comunitat de origen
            j0 = 0;
            i0 = j0+1;
        }
        else j0 = j0 + 1; // sino agafem la seguent comunitat de desti
    }
   
    
    vector<int> temps(4,0);
    for (int i = i0; i < n; ++i) {
        for (int j = j0; j < n; ++j) {
            if (i == j) cout << "punt amb sí mateix" << endl; // La distància a si mateix és 0
            else if(symmetric && i>j) {
                cotxe[i][j] = cotxe[j][i]; // no perdre temps tornant a calcular valors simètrics
                metro[i][j] = metro[j][i];
                peu[i][j] = peu[j][i];
                bici[i][j] = bici[j][i];
                
            }
            else {
                string origen = locations[i][2] + "," +  locations[i][3];
                string desti = locations[j][2] + "," + locations[j][3];

                cout << "punt"<< i << ": (" + origen + ") punt"<< j <<": (" + desti + ")" << endl;  
                
                if(origen != desti) {  
                    temps = getTravelTimeGmaps(origen, desti, debug); // Aquesta funció hauria d'omplir el resultat
                }
                cotxe[i][j] = temps[0];
                metro[i][j] = temps[1];
                peu[i][j] = temps[2];
                bici[i][j] = temps[3];
            }
            
           

            // escrivint als fitxers els temps trobats:
            WriteToFileSimple(to_string(i)+","+to_string(j)+","+to_string(cotxe[i][j]),outputDistCotxe);
            WriteToFileSimple(to_string(i)+","+to_string(j)+","+to_string(metro[i][j]),outputDistMetro);
            WriteToFileSimple(to_string(i)+","+to_string(j)+","+to_string(peu[i][j]),outputDistPeu);
            WriteToFileSimple(to_string(i)+","+to_string(j)+","+to_string(bici[i][j]),outputDistBici);
            // Suposant que podem modificar getTravelTime perquè retorni el valor:
            // matrix[i][j] = getTravelTime(origin, destination);
        }
        j0 = 0;
    }
    
    // return {cotxe, metro, peu, bici};
}

int main() {


   
    string MatriuDCotxe="../output/MatriuDCotxe_"+currentDate+".csv";
    string MatriuDMetro="../output/MatriuDMetro_"+currentDate+".csv";
    string MatriuDPeu="../output/MatriuDPeu_"+currentDate+".csv";
    string MatriuDBici="../output/MatriuDBici_"+currentDate+".csv";

    // vector<string> adreces = readCsv(fitxer);
    vector<vector<string>> coords = readCsvToMatrixFree(inputfile);// id, adreça, lat, lon

    string adreces_amb_coords= "";
    string adreces_perdudes= "";

    int n = coords.size();

    vector<vector<int>> cotxe(n, vector<int>(n, 0.0)), peu(n, vector<int>(n, 0.0)), metro(n, vector<int>(n, 0.0)), bici(n, vector<int>(n, 0.0));

    // buida els fitxers on escriuren tot el rato linies:
    // WriteToFileOver("",outputDistCotxe);
    // WriteToFileOver("",outputDistMetro);
    // WriteToFileOver("",outputDistPeu);
    // WriteToFileOver("",outputDistBici);

    
    vector<vector<string>> sub_v(coords.begin(), coords.begin() + n);
    cout << "adreces que calcularem la matriu de distàncies:" << endl;
    Output2DVectorString(sub_v);

    string ultimOrig, ultDest;
    llegirUltimaLiniaCSV(outputDistCotxe,ultimOrig, ultDest);
    cout << "ultimes comunitats calculades: " << ultimOrig << ", " << ultDest << endl;

    
    DistanceMatrixes(cotxe, metro, peu, bici, sub_v, ultimOrig, ultDest, true, true);

        // aqui guardem les matrius de distancies al final, en fitxers diferents
    // cout << "matriu distancia cotxes:" << endl;
    // Output2DVectorInt(cotxe);
    // cout << "guardant matriu cotxes...:" << endl;
    // Write2DvectorInt(cotxe, MatriuDCotxe);

    // cout << "matriu distancia metro:" << endl;
    // Output2DVectorInt(metro);
    // cout << "guardant matriu metro...:" << endl;
    // Write2DvectorInt(metro, MatriuDMetro);

    // cout << "matriu distancia peu:" << endl;
    // Output2DVectorInt(peu);
    // cout << "guardant matriu peu...:" << endl;
    // Write2DvectorInt(peu, MatriuDPeu);

    // cout << "matriu distancia bici:" << endl;
    // Output2DVectorInt(bici);
    // cout << "guardant matriu bici...:" << endl;
    // Write2DvectorInt(bici, MatriuDBici);

    // for(int i=0; i<num_punts; ++i) {
    //     for(int j=0; j<num_punts; ++j) {
    //         cout << "distancia de " + sub_v[i][0] + " a " + sub_v[j][0] +":" << endl;
    //         double time = getTravelTimeGmaps(sub_v[i][2]+","+sub_v[i][3],sub_v[j][2]+","+sub_v[j][3]);
    //     }        
    // }
            // double time = getTravelTimeGmaps("41.364960,2.118542","41.606921,2.285211");

    // vector<vector<double>> matDistancies = DistanceMatrix(sub_v);
    // cout << "matriu de distàncies: " << endl;
    // Output2DVectorDouble(matDistancies); 

    

    return 0;
}
