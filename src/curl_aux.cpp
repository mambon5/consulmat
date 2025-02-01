#include "curl_aux.h"

string DownloadWebBody(const string& url) {
    CURL *curl = curl_easy_init();
    string webContent;
    if(curl) {
        CURLcode res;
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &webContent);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);     
        if (res != CURLE_OK) {
            cerr << "Failed to download web content: " << curl_easy_strerror(res) << endl;
            webContent.clear();
        }   
    }
    
    return webContent;
}

// Define the write callback function
size_t WriteCallback(void* ptr, size_t size, size_t nmemb, string* userdata) {
    size_t totalSize = size * nmemb;
    userdata->append(static_cast<char*>(ptr), totalSize);
    return totalSize;
}


// Function to download content from a URL using libcurl
std::string DownloadWebContent(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string webContent;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &webContent);
        // cout << "all curl_easy_setopt() done efore easy_perform()" << endl;
        res = curl_easy_perform(curl);
        // cout << "curl_easy_perform() done" << endl;
        if (res != CURLE_OK) {
            cerr << "Failed to download web content: " << curl_easy_strerror(res) << endl;
            webContent.clear();
        }

        curl_easy_cleanup(curl);
    }
    std::cout << "DownloadWebContent() succeded" << endl;
    return webContent;
}

std::string DirectWebContent(std::string& searchGroup, std::string B, std::string  C) {
    std::string baseUrl = "https://finance.yahoo.com/lookup/all?s=";
    std::string url = baseUrl + searchGroup + "&t=A&b="+B+"&c="+C;
    std::string webContent = DownloadWebContent(url);
    return webContent;
}