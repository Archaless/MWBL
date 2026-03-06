Raspi Setup: 

Plug AION640 into a USB Type 3.0 Port 
NOTE: WILL NOT WORK IN A 2.0 PORT

Unpack arm8 files 

Move libDALProxyIrqLA640USB.so.2.1.0 to /usr/local/lib

Run: sudo ln -s /usr/local/lib/libDALProxyIrqLA640USB.so.2.1.0 /usr/local/lib/libDALProxyIrqLA640USB.so

sudo ln -s /usr/local/lib/libDALProxyIrqLA640USB.so.2.1.0 /usr/local/lib/libDALProxyIrqLA640USB.so.2

sudo ln -s /usr/local/lib/libDALProxyIrqLA640USB.so.2.1.0 /usr/local/lib/libDALProxyIrqLA640USB.so.2.1

Run: sudo ldconfig

Run: sudo nano /etc/udev/rules.d/99-aion640.rules 

Add: SUBSYSTEM=="usb", ATTR{idVendor}=="2f45", ATTR{idProduct}=="2014", MODE="0666" 

Run: lsusb and double check VID:PID – 2f45:2014 

Run: sudo udevadm control --reload-rules 

sudo udevadm trigger 

Unplug/Replug Camera 
 

libusb setup: 

Due to incompatibilities with the SDK’s libusb dependencies and the most recent versions of libusb, we must install a local version that is supported. 

Make and cd into desired folder ie. “/home/pi/Documents/AION/libusb” 

Run: sudo apt update

sudo apt install libudev-dev autotools-dev autoconf 

wget https://github.com/libusb/libusb/releases/download/v1.0.23/libusb-1.0.23.tar.bz2 

tar xf libusb-1.0.23.tar.bz2 

cd libusb-1.0.23 

./configure --prefix=/opt/libusb-1.0.23 

make -j 

sudo make install 

NOTE: The actual necessary install will be in: “/opt/libusb-1.0.23/lib”; you don’t need to keep the files we just downloaded and built.  




Compile cpp programs using:  

g++ take_photo_AION640.cpp -L/usr/local/lib -lDALProxyIrqLA640USB -o take_photo

NOTE: Add: `pkg-config --cflags --libs opencv4` to build args if using opencv library 

Run compiled program with: LD_LIBRARY_PATH=/opt/libusb-1.0.23/lib ./*compiled_program* 

Run: ldd ./*your_file* and ensure there are no missing links

DO NOT: Terminate program with ^Z, it will break libusb stuff and seg fault. You will need to, at least, restart the terminal. 

DO NOT: Run multiple instances of anything using the camera at a single time; you will break and seg fault.