#include <iostream>
#include <cstdint>
#include <fstream>
#include <atomic>
#include <thread>
#include <mutex>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <cstring>

#include <opencv2/opencv.hpp>
#include "DALProxyIrqLA640USB.h"

using namespace DALProxyIrqLA640USB_namespace;

// -----------------------------------------------------------------------------
// Constants
// -----------------------------------------------------------------------------
#define IRIMAGE_NBPIXELS        (640 * 512)
#define IRIMAGE_META_TEMP      2
#define IRIMAGE_META_COUNTER   8
#define GETIMAGE_TIMEOUT 5000

// -----------------------------------------------------------------------------
// Shared state
// -----------------------------------------------------------------------------
std::atomic<bool> stop{false};
std::mutex frameMutex;

uint16_t latestImage[IRIMAGE_NBPIXELS * 2];
uint16_t latestMeta[268];
bool hasFrame = false;

// -----------------------------------------------------------------------------
// Capture thread
// -----------------------------------------------------------------------------
void capture_thread(HANDLE handle)
{
    using clock = std::chrono::steady_clock;
    auto next = clock::now();

    while (!stop.load()) {
        next += std::chrono::milliseconds(33); // ~30 FPS

        uint16_t image[IRIMAGE_NBPIXELS * 2];
        uint16_t meta[268];

        auto rc = ProxyIrqLA640USB_GetImage(
            handle, image, meta, GETIMAGE_TIMEOUT
        );

        if (rc != eProxyIrqLA640USBSuccess) {
            std::cerr << "Capture error\n";
            stop.store(true);
            break;
        }

        {
            std::lock_guard<std::mutex> lock(frameMutex);
            std::memcpy(latestImage, image, sizeof(image));
            std::memcpy(latestMeta, meta, sizeof(meta));
            hasFrame = true;
        }

        std::this_thread::sleep_until(next);
    }

    ProxyIrqLA640USB_DisconnectFromModule(handle);
}

int main()
{
    // Connect to camera (same as before)
    HANDLE handle = nullptr;
    int count = 0;

    ProxyIrqLA640USB_GetModuleCount(&count);
    ProxyIrqLA640USB_ConnectToModule(0, &handle, 1);

    ProxyIrqLA640USB_SetFloatFeature(handle, efFrameRate, 30.0f);
    ProxyIrqLA640USB_SetAGCProcessing(handle, eNoAGC);

    std::thread capture(capture_thread, handle);

    // Live feed loop
    cv::namedWindow("IR Live Feed", cv::WINDOW_NORMAL);

    while (!stop.load()) {
        cv::Mat frame16;
        {
            std::lock_guard<std::mutex> lock(frameMutex);
            if (!hasFrame)
                continue;

            // Wrap raw buffer (no copy)
            frame16 = cv::Mat(
                512, 640, CV_16UC1, latestImage
            ).clone(); // clone so mutex can unlock
        }

        // Convert 16-bit -> 8-bit for display
        cv::Mat frame8;
        double minVal, maxVal;
        cv::minMaxLoc(frame16, &minVal, &maxVal);

        frame16.convertTo(
            frame8,
            CV_8UC1,
            255.0 / (maxVal - minVal),
            -minVal * 255.0 / (maxVal - minVal)
        );

        cv::imshow("IR Live Feed", frame8);

        // 1 ms wait → keeps window responsive
        if (cv::waitKey(1) == 27) { // ESC
            stop.store(true);
            break;
        }
    }
    /*while (!stop.load()) {
        {
            std::lock_guard<std::mutex> lock(frameMutex);
            if (!hasFrame) {
                continue;
            }

            uint64_t sum = 0;
            for (int i = 0; i < IRIMAGE_NBPIXELS; ++i)
                sum += latestImage[i];

            auto counter =
                *reinterpret_cast<unsigned short*>(
                    latestMeta + IRIMAGE_META_COUNTER
                );

            std::cout << "\rLive frame "
                      << counter
                      << " avg=" << (sum / IRIMAGE_NBPIXELS)
                      << std::flush;
        }

        std::this_thread::sleep_for(
            std::chrono::milliseconds(30)
        );
    }*/

    std::cout << "\nStopping...\n";
    capture.join();
}

