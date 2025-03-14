#include <iostream>
#include <string>
#include <curl/curl.h>
#include <json/json.h>
#include <unistd.h> // Per a sleep()
#include "textProcess.h"
#include <regex>
// compilar usant
// g++ dates.cpp textProcess.cpp calcula_distancies.cpp -o calcul_dist -I/usr/include/jsoncpp -ljsoncpp -lcurl

using namespace std;

// extreu les coordenades a partir de la URL de google maps:
std::pair<double, double> extractCoordinates(const std::string& url) {
    std::regex regexPattern(R"(@([-+]?\d*\.\d+),([-+]?\d*\.\d+))");
    std::smatch match;

    if (std::regex_search(url, match, regexPattern) && match.size() >= 3) {
        double latitude = std::stod(match[1].str());
        double longitude = std::stod(match[2].str());
        return {latitude, longitude};
    } else {
        throw std::runtime_error("No s'han trobat coordenades a la URL.");
    }
}

std::string obtenirGoogleMapsURL(const std::string& adreca) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;
    string outFile = "output/gmapsout.out" ;
    
    curl = curl_easy_init();
    if (curl) {
        std::string url = "https://www.google.com/maps/search/?q=" + urlencode(adreca);
        // std::string url = "https://www.google.com/search?q=" + urlencode(adreca);
        
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
            std::cerr << "Error HTTP: " << curl_easy_strerror(res) << std::endl;
            return "";
        }
    }

    // Buscar la primera URL de Google Maps dins l’HTML
    std::regex mapsRegex(R"(https:\/\/www\.google\.com\/maps\/preview\/place\/[^"]+)");
    std::smatch match;
    if (std::regex_search(readBuffer, match, mapsRegex)) {
        return match.str(0); // Retorna la primera coincidència
    }

    return "No trobada";
}

std::vector<std::string> extractAddresses(const std::vector<std::vector<std::string>>& matrix) {
    std::vector<std::string> addresses;
    
    for (const auto& row : matrix) {
        if (row.size() >= 5) { // Comprovar que té prou columnes
            std::string fullAddress = trim(row[5]) + " " + trim(row[6]) + " " + trim(row[2]) + " " + trim(row[3])  + " " + trim(row[4]); 
            addresses.push_back(fullAddress);
        }
    }

    return addresses;
}


size_t WriteCallback2(void* contents, size_t size, size_t nmemb, std::string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

// Funció per obtenir coordenades a partir d'una adreça mitjançant Google Maps sense API key
std::string getCoordinates(const std::string& address) {
    std::string mapsURL = obtenirGoogleMapsURL(adreca);
    auto [lat, lon]=  extractCoordinates(mapsURL);
    return  lat +"," + lon;
}

// Funció per obtenir coordenades a partir d'una adreça mitjançant Nominatim
std::string getCoordinates_old(const std::string& address) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;
    
    // URL de Nominatim per a geocodificar adreces
    std::string url = "https://nominatim.openstreetmap.org/search?q=" + std::string(curl_easy_escape(curl, address.c_str(), address.length())) + "&format=json";

    curl = curl_easy_init();
    if (curl) {
         // Afegir headers per evitar bloquejos
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "ElMeuApp/1.0 (contacte@exemple.com)");
        curl_easy_setopt(curl, CURLOPT_REFERER, "https://exemple.com/");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback2);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Error en la petició de geocodificació: " << curl_easy_strerror(res) << std::endl;
            return "";
        }
        curl_easy_cleanup(curl);
    }
    
    // Imprimir la resposta de Nominatim
    // std::cout << "Resposta de Nominatim: " << readBuffer << std::endl;

    // Analitzar la resposta JSON per obtenir les coordenades
    Json::CharReaderBuilder reader;
    Json::Value jsonData;
    std::string errors;

    std::istringstream stream(readBuffer);
    // cout << "hem arribat fins aqui 1" << endl;
    if (Json::parseFromStream(reader, stream, &jsonData, &errors)) {
        // cout << "hem arribat fins aqui 2" << endl;
        if (jsonData.size() > 0) {
            // cout << "hem arribat fins aqui 3: lat:" << jsonData[0]["lat"] << endl;
             // Asegurar-se que els valors de latitud i longitud siguin números
            std::string latStr = jsonData[0]["lat"].asString();
            std::string lonStr = jsonData[0]["lon"].asString();

            // Intentar convertir les cadenes a double
            double lat = 0.0;
            double lon = 0.0;

            try {
                lat = std::stod(latStr);
                lon = std::stod(lonStr);
            } catch (const std::invalid_argument& e) {
                std::cerr << "Error en la conversió de coordenades: " << e.what() << std::endl;
                return "";
            }
            // cout << "hem arribat fins aqui 4" << endl;
            return std::to_string(lon) + "," + std::to_string(lat); // Retorna les coordenades en format lon,lat
        } else {
            std::cerr << "No s'ha trobat cap resultat per l'adreça." << std::endl;
            return "";
        }
    } else {
        std::cerr << "Error en l'anàlisi del JSON de Nominatim: " << errors << std::endl;
        return "";
    }
}

// Funció per obtenir el temps de viatge entre dues coordenades amb OSRM
void getTravelTime(const std::string& origin, const std::string& destination) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    // amb cotxe
    std::string url = "http://router.project-osrm.org/route/v1/driving/" + origin + ";" + destination + "?overview=false";

    // a peu
    // std::string url = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/" + origin + ";" + destination + "?steps=true&overview=full";
    
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback2);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Error en la petició: " << curl_easy_strerror(res) << std::endl;
        } else {
            
            // cout <<"resposta osrm: " << endl << readBuffer << endl;

            // Analitzar la resposta JSON
            Json::CharReaderBuilder reader;
            Json::Value jsonData;
            std::string errors;

            std::istringstream stream(readBuffer);
            if (Json::parseFromStream(reader, stream, &jsonData, &errors)) {
                if (!jsonData["routes"].empty()) {
                    int duration = jsonData["routes"][0]["duration"].asInt();
                    std::cout << "Temps de viatge: " << duration / 60 << " minuts" << std::endl;
                } else {
                    std::cerr << "No s'han trobat rutes." << std::endl;
                }
            } else {
                std::cerr << "Error en l'anàlisi del JSON: " << errors << std::endl;
            }
        }
        curl_easy_cleanup(curl);
    }
}

int main() {
    std::string originAddress = "ALGUER, 32, Granollers, Barcelona";
    std::string destinationAddress = "ALFONS IV, 55 Granollers, barcelona";

    // Obtenir coordenades per les adreces
    std::string originCoords = getCoordinates(originAddress);
    std::string destinationCoords = getCoordinates(destinationAddress);

    string inputfile="input/Comunidades.csv";
    string outputCoords="output/Comunidades_coords.csv";
    string outputPerdudes="output/Comunidades_perdudes.csv";
    string outputDistances="output/Comunidades_dist.csv";
    // vector<string> adreces = readCsv(fitxer);
    vector<vector<string>> adreces2 = readCsvToMatrixFree(inputfile, 3);
    OutputVector(adreces2[4]);
    cout << "holiwis"<<endl;

    std::vector<std::string> addresses = extractAddresses(adreces2);
    Output2DVectorString(adreces2);
    cout << "modificacio final:" << endl;
    OutputVector(addresses);
    

    std::string adreca = "APELES MESTRE 2B 08402 GRANOLLERS BARCELONA";
    std::string mapsURL = obtenirGoogleMapsURL(adreca);
    auto [lat, lon]=  extractCoordinates(mapsURL);
    cout << "latitud: " << lat << ", longitud: " << lon << endl;
 
    std::cout << "Google Maps URL: " << mapsURL << std::endl;
    return 0;


    string output= "";
    string adreces_perdudes= "";
    int i = 0;
    for(string adreça : addresses) {
        ++i;
        if(i > 20) break;
        // Obtenir coordenades per les adreces
        sleep(2);
        std::string originCoords = getCoordinates(adreça);
        
        if (!originCoords.empty()) {            
            output = output + adreça +"," + originCoords + "\n";
            
        }
        else {
            adreces_perdudes = adreces_perdudes + adreça +"\n";
        }
        cout << adreça + "," + originCoords << endl;
    }
    cout << "adreces trobades: " << endl;
    cout << output<< endl;

    cout << "adreces perdudes: " << endl;
    cout << adreces_perdudes<< endl;

    if (!originCoords.empty() && !destinationCoords.empty()) {
        std::cout << "Coordenades d'origen: " << originCoords << std::endl;
        std::cout << "Coordenades de destí: " << destinationCoords << std::endl;

        // Obtenir el temps de viatge amb OSRM
        getTravelTime(originCoords, destinationCoords);
    }

    return 0;
}
