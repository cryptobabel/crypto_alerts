This set of scripts creates and controls a blinking notification for Cryptocurrency, such as Bitcoin, price alerts.


Intended to be an educational documentation displaying how combining different technologies can acheive
a simple yet useful tool. 


A Teensy/Arduino board controls the LEDs (in my case installed in an Android figurine) 
and listens on the hosts computer comport via its USB interface. 

Python is used as the front end to make requests to check 'coinmarketcap' for Bitcoin prices and
relay that back to the Teensy board. 

Utilizing cryptoalert.py and the setup.py a Windows based application can be created so it can be added to run at
start in the background. 


You may need to update the comport as well as the output LED pins to fit your appliation, otherwise should run as-is. 
If running in the background with py2exe set your default values in cryptoalert.py and build the exe.

You can configure the type of alert, price targets and other settings in config.ini

# Build exe you can add to startup

http://www.py2exe.org/

python setup.py py2exe


# Requirements
Python environment: https://docs.python.org/3/using/windows.html
Arduino development environment/IDE https://www.arduino.cc/en/Guide/Windows
Teensy plugins/tools (optional if not using teensy board) https://www.pjrc.com/teensy/teensyduino.html

# Python requirements: 
coinmarketcap https://pypi.python.org/pypi/coinmarketcap/
 
