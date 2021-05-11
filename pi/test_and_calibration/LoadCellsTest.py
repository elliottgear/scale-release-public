#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

"""
This CLI based program is for testing the load cells, by taking an expected weight and then
taking the measured weight and comparing to the actual weight.
"""

# SETTINGS
referenceUnit = -23.139838974
samplesToTake = 10

import time
import sys
import RPi.GPIO as GPIO
from pi.hx711 import HX711
import statistics
from colorama import Fore, Style


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def getWeight():
    val = hx.get_weight(5)
    val = val / 1000
    val = val * -1
    if val < 0:
        val = 0
    print(val)
    hx.power_down()
    hx.power_up()
    time.sleep(0.05)
    return val

hx = HX711(21, 20)
#hx = HX711(6,5)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Please add the weight for testing now, waiting 5 seconds...")
time.sleep(0)

print('*** Scale testing software for Wifi Enhanced Electronic Scale ***')
print('Using reference value of: ' + str(referenceUnit))
expectedValue = input('Enter actual weight in kg: ')
print('Collecting weights...')
time.sleep(1)
weights = []

start_time = time.time()
for i in range(samplesToTake):
    weights.append(getWeight())
print("--- %s seconds to measure---" % (time.time() - start_time))
print('\n \n')
print('Weights Collected')

## Calculate the values we care about
mean = sum(weights) / len(weights)
median = statistics.median(weights)
variance = sum([((x - mean) ** 2) for x in weights]) / len(weights)
std = variance ** 0.5
minimum = min(weights)
maximum = max(weights)
diffMean = float(expectedValue) - mean
diffMed = float(expectedValue) - median

# TODO: Make this print to a text file for diagnostic purposes and logging
print('********** RESULTS **********')
if abs(diffMean) < 0.29:
    print(Fore.GREEN + 'Result: passed')
else:
    print(Fore.RED + 'Result: failed')
print(print(Style.RESET_ALL))
print('Expected value: ' + str(expectedValue))
print(str(len(weights)) + ' values collected')
print('Mean of collected values: ' + str(mean))
print('Standard deviation of values: ' + str(std))
print('Max collected value: ' + str(minimum))
print('Min collected value: ' + str(maximum))
print('Difference from expected value: ')
print('     (expected - mean of collected): ' + str(diffMean))
print('     (expected - median of collected): ' + str(diffMed))


cleanAndExit()
