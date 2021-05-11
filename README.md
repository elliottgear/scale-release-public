- Repo @ https://github.com/elliottgear/scale-release-public
# WiFi Enhanced Electronic Scale

## Description
This project was created as a part of the University of Vermont College of Engineering
Senior Design Capstone Program. The WiFi Enhanced Electronic Scale is a project sponsored
by Dr. Jean Harvey to create a WiFi connected scale for in home weight loss studies.

This entire project is designed to run on a Raspberry Pi (shortened to Pi in this document) using Python3 and Arduino 
connected to the Pi. The files in the 'data' folder are designed to be run on a server or another system
that is up 24/7 to collect data and automagically enter it into RedCap since in our testing 
we were unable to get the Pi to reliably write to RedCap directly. 

## File List
This is a complete listing of all files in the project along with a sort description of their
function(s), a more detailed description can be found in files. ALL Pi programs that interface with the
HX711 expect it to be connected to GPIO pins 20 and 21, use of other pins will require reconfiguration
of the code.
- Folder: **arduino** contains all Arduino code to drive fingerprint scanner see instructions below for compiling and run
instructions. Each sketch is in its own folder as required by the Arduino compiler.
    - **FPS_Enroll.ino** Used to save a user's fingerprint to the internal memory of the finger print scanner. The slot
    which the user's print is stored can be changed by modifying the code, there are 200 slots to save a print in.
    - **FPS_IDFinger.ino** Detects finger on the scanner, and then returns 1, 2 or 3 to the serial port to represent waiting,
    positive identification or negative ID, respectively. 
    - **Libraries** The finger print scanner library and framework, move the contents of this folder to wherever
    your Arduino compiler expects libraries to be stored.
- Folder: **data** contains all code related to sending and receiving. These files must be run on a 
separate system such as a server since they do not run correctly on a Pi.
data to Thingspeak and RedCap
    - **read_thingspeak.py** checks Thingspeak database every 10 seconds for new data, if
    there is new data it pulls all datapoints, and calls the redcap_writter.py to send the data
    to RedCap.reads the data sent from the scale to Thingspeak, and calls a function to write fresh
    data collected into RedCap.
    - **redcap_writter.py** contains the functions to write data into a RedCap survey data collected
    using Selenium and Chromedriver. These were used instead of the official RedCap API since it does not
    support a way to easily enter one data point at a time and is designed for bulk data ingestion. 
- Folder: **pi** contains all code designed to run on the Pi. All is written in python3 and any 
libraries not included in base install of Raspbian are included.
    - **hx711.py** the HX711 library to interface with the loadcell amp through the Pi
    GPIO pins
    - **Scale.py** a CLI based version of the scale general interface for hardware testing over SSH
    - **Scale_GUI.py** the main driver program of the scale with a full screen Tkinter GUI. 
    This file is launched at boot. When running in fullscreen mode it can be quit by pressing the 'a' key.
    - **send_data.py** contains the functions called from Scale_GUI.py which send
    the scale data to Thingspeak which is a intermediary Database since data cannot
    be sent directed from the Pi to RedCap due to Selenium compatibility issues.
    - Folder: **test_and_calibration** for testing and calibration of scale and associated hardware. 
        - **CalLoadCells.py** Reads the raw value from the HX711 amp and averages the value to help
        calibrate the scale with a load on it
        - **DataLogger.py** Writes the Unix system time and the raw loadcell values to a CSV used for 
        testing of loadcells. Specifically used in structural testing to compare loadcell specs with real
        world use. 
        - **hx711.py** the HX711 library to interface with the loadcell amp through the Pi
        GPIO pins
        - **LoadCellsTest.py** a full CLI program which reads the load cells in KG and compares the reading against
        an entered known value and prints whether the load cells passed the test as specified in the engineering
        specs
        - **OG.py** original load cell reader as found in HX711 library. Used in worst cases for seeing if the problem is
        hardware or software related. 
## RPI Setup and Configuration
1. Acquire the preferable hardware, configure as described in technical documentation
    - Computer: Raspberry Pi 3B
        - The ZeroW DOES work however we found does not produce a
        responsive GUI. 
    - Screen: UCTRONICS 3.5in LCD or similar. Changing to a different model will require modificaiton of the resolution
    of the GUI window.
        - After install of OS on the Pi, use the most recent documentation
         included with the screen to instal drivers while using an external HDMI
         monitor as most of these LCDs do not work out of the box without drivers.
2. The current release of 32 bit Rasbian should be burned to an
SD card with Raspberry Pi Imager.
    - This includes everything the scale will need to run.
3. Click the top left corner and open raspberry pi configuration and
change the following
    - turn off auto sleep
    - turn on SSH
    - connected to WiFi (the Pi has shakey at best support for WPA Enterprise which
    is what UVM uses.)
4. Pull the repo to the Pi. 
    ```
    git pull https://github.com/elliottgear/scale-release.git
    ```
5. Modify the /etc/profile file to boot the GUI on startup
    ```
   sudo nano /etc/profile
   sudo python3 '*path to Scale_GUI.py*' example: /user/Desktop/scale_release/Scale_GUI.py
   ```
6. Reboot
    ```
    sudo reboot
    ```
7. After reboot the scale *should* boot into the scale GUI, if this does not happen try to manually launch the program with
    ```
   python3 Scale_GUI.py
   ```
    Which will readout the error messages in the terminal.


## Arduino Setup and Configuration
- Use an Arduino Nano or like clone
- Load the Arduino sketch located in scale-release/arduino to the using the official Arduino IDE.
- In the current configuration the enroll and read programs have to be loaded separately, these should be combined to allow
research subjects to self enroll themselves. 
- After the loading of either program onto the Arduino use the serial monitor to confirm that it is outputting as expected.

