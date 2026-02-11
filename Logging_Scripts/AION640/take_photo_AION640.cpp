#include <iostream>
#include <cstdint>
#include <fstream>
#include <chrono>
#include <thread>
#include <ctime>
#include <iomanip>
#include <sstream>

#include "DALProxyIrqLA640USB.h"

using namespace DALProxyIrqLA640USB_namespace;

// -----------------------------------------------------------------------------
// Camera constants
// -----------------------------------------------------------------------------
#define IRIMAGE_NBPIXELS        (640 * 512)
#define IRIMAGE_META_TEMP      2
#define IRIMAGE_META_TIMESTAMP 11
#define IRIMAGE_META_COUNTER   8

#define GETIMAGE_TIMEOUT 5000

// -----------------------------------------------------------------------------
// Image buffers
// -----------------------------------------------------------------------------
uint16_t paImage[IRIMAGE_NBPIXELS * 2];
uint16_t paMeta[268];

// -----------------------------------------------------------------------------
// UTC timestamp string
// -----------------------------------------------------------------------------
std::string utc_timestamp()
{
    std::time_t t = std::time(nullptr);
    std::tm tm = *std::gmtime(&t);

    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y%m%d-%H%M%S");
    return oss.str();
}

// -----------------------------------------------------------------------------
// Main
// -----------------------------------------------------------------------------
int main(int argc, char* argv[])
{
    // -------------------------------------------------------------------------
    // USER SETTINGS
    // -------------------------------------------------------------------------
    int burstCount = 1;                 // 1 = single photo, N = burst
    int burstDelayMs = 100;             // delay between shots
    float frameRate = 30.0f;

    // Optional CLI override: ./app 10
    if (argc > 1)
        burstCount = std::stoi(argv[1]);

    // -------------------------------------------------------------------------
    // Connect to camera
    // -------------------------------------------------------------------------
    int moduleCount = 0;
    HANDLE handle = nullptr;

    auto rc = ProxyIrqLA640USB_GetModuleCount(&moduleCount);
    if (rc != eProxyIrqLA640USBSuccess || moduleCount == 0) {
        std::cerr << "No camera modules found\n";
        return 1;
    }

    char name[300]{};
    ProxyIrqLA640USB_GetModuleName(0, name, sizeof(name));
    std::cout << "Connecting to: " << name << "\n";

    rc = ProxyIrqLA640USB_ConnectToModule(0, &handle, 1);
    if (rc != eProxyIrqLA640USBSuccess) {
        std::cerr << "Failed to connect\n";
        return 1;
    }

    // Camera configuration
    ProxyIrqLA640USB_SetNUCProcessing(handle, 1, 0);
    ProxyIrqLA640USB_SetFloatFeature(handle, efFrameRate, frameRate);
    ProxyIrqLA640USB_SetAGCProcessing(handle, eNoAGC);

    // -------------------------------------------------------------------------
    // Capture loop
    // -------------------------------------------------------------------------
    std::cout << "Capturing " << burstCount << " image(s)...\n";

    for (int i = 0; i < burstCount; ++i) {
        rc = ProxyIrqLA640USB_GetImage(
            handle, paImage, paMeta, GETIMAGE_TIMEOUT
        );

        if (rc == eProxyIrqLA640USBCommFailed) {
            std::cerr << "USB communication lost\n";
            break;
        }

        if (rc != eProxyIrqLA640USBSuccess) {
            std::cerr << "Capture error: "
                      << ProxyIrqLA640USB_GetErrorString(rc) << "\n";
            continue;
        }

        // Compute average pixel value
        uint64_t sum = 0;
        for (int p = 0; p < IRIMAGE_NBPIXELS; ++p)
            sum += paImage[p];

        auto frameCounter =
            *reinterpret_cast<unsigned short*>(paMeta + IRIMAGE_META_COUNTER);

        auto temperature =
            *reinterpret_cast<float*>(paMeta + IRIMAGE_META_TEMP);

        std::cout << "Frame " << i
                  << " | Counter: " << frameCounter
                  << " | Avg: " << (sum / IRIMAGE_NBPIXELS)
                  << " | Temp: " << temperature << " C\n";

        // Save image immediately
        std::string filename =
            "/home/pi/Documents/AION/pics/imgRAW_" +
            utc_timestamp() +
            "_frame" + std::to_string(i) + ".bin";

        std::ofstream out(filename, std::ios::binary);
        out.write(reinterpret_cast<char*>(paImage),
                  IRIMAGE_NBPIXELS * sizeof(uint16_t));
        out.close();

        // Delay between frames (burst pacing)
        if (i + 1 < burstCount)
            std::this_thread::sleep_for(
                std::chrono::milliseconds(burstDelayMs)
            );
    }

    // -------------------------------------------------------------------------
    // Cleanup
    // -------------------------------------------------------------------------
    ProxyIrqLA640USB_DisconnectFromModule(handle);
    std::cout << "Done.\n";

    return 0;
}
