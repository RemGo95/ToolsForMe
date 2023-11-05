#include <iostream>
#include <fstream>
#include <string>
#include <mutex>
#include <opencv2/core.hpp>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>
#include <opencv2/dnn/dnn.hpp>
#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "inih/INIReader.h"

// Create a global logger
std::shared_ptr<spdlog::logger> logger;

struct CSVData {
    // Define fields to store your CSV data.
};

void setupLogger(const INIReader& config) {
    std::string logFile = config.Get("Logging", "LogFile", "application.log");
    std::string logLevel = config.Get("Logging", "LogLevel", "all");

    // Create a logger with a file sink and log level based on the config file.
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(logFile, true);
    logger = std::make_shared<spdlog::logger>("app_logger", file_sink);

    if (logLevel == "errors") {
        logger->set_level(spdlog::level::err);
    } else {
        logger->set_level(spdlog::level::trace);
    }
}

void readCSVData(const std::string& filename, CSVData& data, std::mutex& dataMutex) {
    try {
        std::ifstream file(filename);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open CSV file.");
        }

        // Read and parse data from the CSV file and store it in data.
        //HANDLE hMutex = CreateMutex(NULL, FALSE, "MyMutex");
//if (hMutex == NULL) {
    // Handle error
//}

// Wait for the mutex
//DWORD dwWaitResult = WaitForSingleObject(hMutex, INFINITE);
//if (dwWaitResult != WAIT_OBJECT_0) {
    // Handle error
//}

// Do something with the file

// Release the mutex
//if (!ReleaseMutex(hMutex)) {
    // Handle error
//}

// Close the mutex handle
//CloseHandle(hMutex);

        // Use dataMutex to protect access to data when reading/writing.

        logger->info("CSV data read successfully.");
    } catch (const std::exception& e) {
        logger->error("Error: {}", e.what());
    }
}

// Add similar logging for other functions.

int main(int argc, char** argv) {
    // Read the configuration file
    INIReader config("config.ini");

    // Initialize the logger based on the configuration
    setupLogger(config);

    try {
        CSVData data;
        std::mutex dataMutex;

        // Read data from the CSV file in a separate thread.
        std::thread csvReader(readCSVData, "your_file.csv", std::ref(data), std::ref(dataMutex));

        // Display camera feed in the main thread.
        displayCameraFeed();

        // Display CSV data in the GUI.
        displayDataInGUI(data);

        // Join the CSV reader thread.
        csvReader.join();
    } catch (const std::exception& e) {
        logger->error("Error: {}", e.what());
    }

    return 0;
}