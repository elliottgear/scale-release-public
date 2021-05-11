#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

'''
Requires the existance of a data.csv file where the raw signals and the
UNIX system time will be logged indefinatly for load and other testing.
This was used for the max load testing of the scale.
'''
import time
import sys
import RPi.GPIO as GPIO
from pi.Scale import scale_setup


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    sys.exit()

def get_time():
    return time.time()

def write_line(contents):
    with open('data.csv', 'a') as fd:
        fd.write(contents + '\n')

def get_weight(hx):
    weight = hx.get_weight()
    weight = weight / 1000
    return weight


def main():
    print('HX711 Data Logger V1.1')
    write_line('New test starts below')
    # setup
    # for running on pi zero
    hx = scale_setup(1, 6, 5)
    #hx = scale_setup(1)
    print('HX711 initialized, ready')
    time.sleep(5)
    print('starting...')

    while True:
        try:
            row_contents = ''
            row_contents = row_contents + str(get_time()) + ', '
            row_contents = row_contents + str(get_weight(hx))
            write_line(row_contents)
            print(row_contents)
            print('datalogged...')

        except(KeyboardInterrupt, SystemExit):
            print('quitting...')
            break

if __name__ == "__main__":
    main()
