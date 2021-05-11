#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

"""
Used for calibrating load cells by taking an average
calibration factor over a number of measurements. Run from
CLI not for patient use. Each unit must be calibrated after
manufacture.
"""
import time
import sys

EMULATE_HX711 = False

# this reference unit was set using a 363g box of
# wire and gives a fairly good reading in kg for
# testing purposes only
referenceUnit = 1


import RPi.GPIO as GPIO
from pi.hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(21, 20)

# these are this way bc this is the way they are
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
# hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")
time.sleep(10)

# to use both channels, you'll need to tare them both
# hx.tare_A()
# hx.tare_B()
readings = 20
vals = []
for i in range(readings):
    try:
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        val = val / 1000
        val = val * -1
        if val < 0:
            val = 0
        vals.append(val)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

mean = sum(vals) / len(vals)
print('mean:')
print(mean)
