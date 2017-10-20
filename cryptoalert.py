import ConfigParser
import os
import serial.tools.list_ports
import signal
import sys
import time

from coinmarketcap import Market

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = ConfigParser.ConfigParser()
config.read(os.path.join(__location__, 'config.ini'))

# Types of alerts
alert_type = config.get('alerts', 'alert_type')

# price_alert enables LED if price_target is reached (int represents USD value above target)
price_target = config.getint('alerts', 'price')

# percentage_alert enables LED if percentage_target is reached (float represents percentage can be negative)
percentage_target = config.getfloat('alerts', 'percentage')

# change_alert enables LED if change_target is reached. (int represents USD value change)
change_target = config.getfloat('alerts', 'change')

# Cryptocurrency
crypto = config.get('default', 'crypto')

# The comport our device is connected to
COMPORT = config.get('serial_connection', 'comport')
# Buad rate of our device
BRATE = config.getint('serial_connection', 'brate')
# Timeout for connecting to our device
DTIMEOUT = config.getint('serial_connection', 'dtimeout')

# The commands we defined to enable and disable our LEDs
ENABLE_CMD = config.get('led_commands', 'enable')
DISABLE_CMD = config.get('led_commands', 'disable')

class Alert:

    def price(self, cmc_data, last):
        # Check if we've met or exceeded target
        
        print("Checking target price")
        enable() if float(
            cmc_data["price_usd"]
            ) >= price_target else disable()

    def percentage(self, cmc_data, last):
        # Calculate percentage based off of last check
        
        print("Checking percentage target")
        diff = (abs(float(
            cmc_data["price_usd"]
            ) - last)/last)*100.0
        enable() if diff >= percentage_target else disable()

    def change(self, cmc_data, last):
        # Simply find the difference and see if we meet or exceed

        print("Checking value change")
        diff = abs(float(cmc_data["price_usd"]) - last)
        enable() if diff > change_target else disable()

# Load function from config option
def call_alert(o, alert_type, cmc_data, last):
    getattr(o, alert_type)(cmc_data, last)

# Handler kill signals to disable LEDs
def handler_stop_signals(signum, frame):
    disable()

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)
 
# Functions to enable or disable the LED
def enable():
    print("Enabling LED")
    ser = serial.Serial(COMPORT, BRATE, timeout=DTIMEOUT)
    ser.write(ENABLE_CMD)
    ser.close()

def disable():
    print("Disabling LED")
    ser = serial.Serial(COMPORT, BRATE, timeout=DTIMEOUT)
    ser.write(DISABLE_CMD)
    ser.close()
    
def main(argv):
    # Track LED state
    enabled = False
    # Track last price
    last = 0.0

    # Instantiate our Alerts
    alert = Alert()

    # Instantiate our connection to CoinMarketCap
    cmc = Market()
    
    print("Crypto Alert is running...")

    # We're going to run forever until destroyed
    while True:
        # Load JSON ticker data
        r = cmc.ticker(crypto)

        # Gather price for tracking
        r_price = float(r[0]["price_usd"])
        
        print("{} Price: {}".format(crypto, str(r_price)))

        # Call our alert
        call_alert(alert, alert_type, r[0], last)

        # Update last price
        last = r_price
            
        # Pause processing. CMC only refreshs every 300 seconds,
        # hardcode timeout for led disable
        # until we code in a different service to make this more useful
        time.sleep(60)
        if enabled:
            disable()

if __name__ == "__main__":
     main(sys.argv)
    
