#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

import serial
import time
from pi.hx711 import HX711

def check_serial_status():
    ## recreate the serial reader everytime idk why but the way we gotta do it
    com_port = '/dev/ttyUSB0'
    serial_reader = serial.Serial(port=com_port, baudrate=9600)
    status = serial_reader.readline()
    # covert to a readable string by stripping off newlines etc
    status = status.split()
    return int(status[0])

def scale_setup(referenceUnit = -24.376304191, port1 = 20, port2= 21):
    hx = HX711(port1, port2)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    return hx

def weigh_user_guest(hx):
    print('taring.')
    # get them off the scale
    while get_weight(hx) > 5:
        print('please step off scale')
        time.sleep(.5)
    hx.tare()
    # wait for them to step back on...
    while get_weight(hx) < 5:
        print('tared please step back on')

    print('stand still... reading your weight')
    weight = get_weight(hx)
    print(weight)
    print('please step off...')
    time.sleep(5)

def get_weight(hx):
    weight = hx.get_weight(5)
    weight = weight/1000
    if weight < 0:
        weight = 0
    return weight

def main():
    # create scale object
    hx = scale_setup()
    print('hello')

    # run forever
    while True:
    # read the finger print scanner when the weight is greater than 5kg
        weight = get_weight(hx)
        print(weight)
        if weight > 5:
            serial_status = check_serial_status()
            print(serial_status)

            # no print found
            if serial_status == 1:
                print('please scan your toe print')

            # print accepted
            elif serial_status == 2:
                print('**********Toe print accepted**********')
                print('Please step off scale to tare')
                time.sleep(2)
                # replace this with a database sender eventually
                # this is fine for testing
                weigh_user_guest(hx)

            # print rejected
            elif serial_status == 3:
                print('Guest user recognized')
                print('Please step off scale to tare')
                time.sleep(2)
                weigh_user_guest(hx)

        else:
            print('sleeping...')
            time.sleep(1)


if __name__ == "__main__":
    main()
