#TODO remove all print statements
#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

from tkinter import *
from tkinter.ttk import *
import urllib.request
from time import strftime, sleep
from pi.hx711 import HX711
import serial
from pi.send_data import send

version = 'WiFi Scale v1.0'
PATIENT_ID = 2494

#%% CONSTANTS / SETTINGS
REF_UNIT = -23.139838974
TRIG_THRESHOLD = 1


# creating tkinter window
root = Tk()
root.title('Wifi Scale')
root.geometry('320x480')
root.config(bg='black')
style = Style(root)
style.configure('TLabel', background='black', foreground='white')
style.configure('TFrame', background='black')

# comment for dev
root.attributes('-fullscreen', True)
root.config(cursor="none")


#%% SCALE INITALIZER FUNCTIONS
""" Creates a global object called HX which can be used to call the loadcells to tare, get vals etc.
Parameters
----------
reference_unit : long, optional
    Reference unit for HX711
port1 : int, optional
    Port 1 of HX711
port2 : int, optional
    Port 2 of HX711
"""
def scale_setup(reference_unit = REF_UNIT, port1 = 21, port2 = 20):
    global hx
    hx = HX711(port1, port2)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(reference_unit)
    hx.reset()
    hx.tare()


""" Gets raw reading from hx and coverts it to kg.
"""
#%% OTHER LOGICAL FUNCTIONS
def read_hx():
    reading = hx.get_weight(5)
    reading = reading / 1000
    reading = round(reading, 2)
    return reading


""" Gets raw reading from hx 3 times, and averages the reading. Also prints to LCD that the weight is being read.
"""
def real_weight():  # TODO add if statements for different calibration ranges
    lbl_main.config(text='Please hold still. \n Reading weight...', font=('calibri', 18))
    root.update()
    samples = []
    for i in range(3):
        samples.append(read_hx())

    # average the samples
    reading = sum(samples) / len(samples)
    print(reading)
    return reading

'''
Checks the current serial reading, then returns the status as an integer.'''
def check_serial_status():
    # recreate the serial reader everytime idk why but the way we gotta do it
    com_port = '/dev/ttyUSB0'
    serial_reader = serial.Serial(port=com_port, baudrate=9600)
    serial_status = serial_reader.readline()
    # covert to a readable string by stripping off newlines etc
    serial_status = serial_status.split()
    return int(serial_status[0])

'''
Tares the HX object to 0'''
def tare():
    lbl_main.config(text='Please step \n off to tare', font=('calibri', 38))
    root.update()
    # wait for them to actually step off anything over 15kg they are probably still on the scale
    while hx.get_weight() > 15:
        print('waiting for step off')
        lbl_main.config(text='Waiting for \n step off...', font=('calibri', 32))
        root.update()
        sleep(.1)
    hx.tare()
    lbl_main.config(text='Please step \n back on', font = ('calibri', 38))
    root.update()

#TODO do these two functions a better way, will be redudent with power off circuitry
"""
blanks the screen by turning all labels to black"""
def blank_all_labs():
    lbl_title.config(foreground='black')
    lbl_time.config(foreground='black')
    lbl_date.config(foreground='black')
    # set the text to '' here so the old weight does not display
    lbl_main.config(foreground='black', text='')
    lbl_unit.config(foreground='black')
    lbl_status.config(foreground='black')
    root.update()

'''
Does the same as above, except sets all the backgrounds to white.'''
def show_all_labs():
    lbl_title.config(foreground='white')
    lbl_time.config(foreground='white')
    lbl_date.config(foreground='white')
    lbl_main.config(foreground='white')
    lbl_status.config(foreground='green')
    root.update()


'''
Updates the time on screen'''
#%% DISPLAY UPDATE FUCTIONS
def sys_time():
    string = strftime('%H:%M %p')
    lbl_time.config(text=string)
    root.update()
    lbl_time.after(1000, sys_time)

'''
Updates the date on screen'''
def date():
    string = strftime('%Y-%m-%d')
    lbl_date.config(text=string)
    root.update()
    lbl_date.after(1000, date)

#TODO figure out why this causes issues
'''
Checks internet connection satus by pinging uvm.edu'''
def status():
    print('checking connection status')
    host = 'http://uvm.edu'
    try:
        urllib.request.urlopen(host)
        lbl_status.config(foreground='green', text='Connected!')
        print('connected')
        root.update()
        lbl_status.after(5000, status)
    finally:
        lbl_status.config(foreground='red', text='Conncetion problem')
        print('connected')
        root.update()
        lbl_status.after(5000, status)

'''
Main logic off the scale, checks for weight on the load cells,
then reads the print and makes decsions from there'''
def update_main():
    reading = read_hx()
    print(reading)

    # there probably isn't someone on the scale
    if TRIG_THRESHOLD >= reading:
        print('nobody on scale...')
        blank_all_labs()
        lbl_main.after(500, update_main)

    # there must be someone on the scale then, wanting to interact
    else:
        show_all_labs()
        # prompt for toeprint reading and start reading...
        # 1 = waiting for reading, 2 = user ID'd, 3 = unidentifed person
        serial_status = 1
        count = 0
        while serial_status == 1:
            serial_status = check_serial_status()
            lbl_main.config(text='Please scan toe', font=('calibri', 18))
            root.update()
            # TODO after 10 seconds set to guest mode automatically
            count = count + 1
            if count > 20:
                serial_status = 3
            if serial_status != 1:
                print('serial isnt 1!!!!')
                break
            # we don't wanna go toooooooooooo fast. slow down the scanner rate here, kinda...
            sleep(.5)

        # the person on the scale is a subject
        if serial_status != 1:
            lbl_main.config(text='Hello, Callan!', font=('calibri', 24))
            root.update()
            sleep(1)
            tare()
            # wait for them to step back on
            while read_hx() < TRIG_THRESHOLD:
                sleep(.1)
            reading = real_weight()
            reading_lb = reading * 2.2
            # display the result and stop everything for 8 seconds
            while read_hx() > 5:
                lbl_main.config(text=str(round(reading_lb, 1)), foreground='white', background='black',
                                font=('calibri', 65))
                lbl_unit.config(foreground='white')
                root.update()
                sleep(1)

            try:
                print('sending to redcap')
                send(PATIENT_ID, reading)
            except:
                print('data send error. ')

            # sleep for 10 after step off to keep weight up on screen
            print('sleeping...')
            sleep(10)
            lbl_main.after(500, update_main)
            # we are done here

        # the person in the scale is a guest
        if serial_status == 3:
            lbl_main.config(text='Guest detected, \n hello!', font=('calibri', 24))
            root.update()
            sleep(1)
            tare()
            while read_hx() < TRIG_THRESHOLD:
                sleep(.1)
            reading = real_weight()
            reading_lb = reading * 2.2
            # display the result and stop everything for 8 seconds
            while read_hx() > 5:
                lbl_main.config(text=str(round(reading_lb, 1)), foreground='white', background='black',
                                font=('calibri', 65))
                lbl_unit.config(foreground='white')
                root.update()
                sleep(1)

            print('sleeping...')
            sleep(10)
            lbl_main.after(500, update_main)
            # we are done here

        # handle some sort of scanner error if the reading isn't 1 2 3
        else:
            lbl_main.config(text='Scanner error \n please step off', font=('calibri', 24))
            root.update()
            lbl_main.after(500, update_main)
            # we are done here


#%% Inital window buildout and packing, call all functions below here.
lbl_title = Label(root, text=version, foreground='white', background='black', font=('helvetica', 18))
lbl_time = Label(root, foreground='white', background='black', font=('helvetica', 12))
lbl_date = Label(root, foreground='white', background='black', font=('helvetica', 12))
lbl_main = Label(root, text='hello', foreground='white', background='black', font=('helvetica', 70))
lbl_unit = Label(root, text='pounds', foreground='white', background='black', font=('helvetica', 35))
lbl_status = Label(root, text='Connected!', foreground='green', background='black', font=('helvetica', 12))

# placing of labels in window in order that they are displayed to avoid issues
lbl_title.pack(side='top')
lbl_time.pack(side='top')
lbl_date.pack(side='top')
lbl_main.place(relx=0.5,
               rely=0.5,
               anchor='center')
lbl_unit.place(relx=0.5,
               rely=0.65,
               anchor='center')
lbl_status.pack(side='bottom')

# call scale setup functions here
scale_setup(REF_UNIT)
check_serial_status()

# call all updaters here to initalizae
sys_time()
date()
update_main()
# this is causing a crash investigate later...
# status()

# let us quit
root.bind("a", lambda x: root.destroy())

mainloop()
