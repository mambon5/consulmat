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


using namespace std;



string DownloadWebBody(const string& url);
size_t WriteCallback(void* ptr, size_t size, size_t nmemb, string* userdata);
std::string DownloadWebContent(const std::string& url);
std::string DirectWebContent(std::string& searchGroup, std::string B, std::string C);
