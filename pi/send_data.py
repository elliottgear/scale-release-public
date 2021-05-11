#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

import random
import urllib.request
import string
import datetime
import time

'''
FIELDS
Field 1: Submission ID
Field 2: Patient ID
Field 3: Weight
Field 4: Date
Field 5: ReadingConf
'''


def send(patientID, weight):
    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'W1LHV4CQO5RHXJU8'
    HEADER = '&field1=' + str(createID()) + '&field2=' + str(patientID) + '&field3=' + str(weight) + '&field4=' + str(getDateTime())
    new_URL = URL + KEY + HEADER
    print(new_URL)

    data = urllib.request.urlopen(new_URL)
    print(data)

def createID():
    # TODO make this more optimized to give a more *random* result
    length = 10
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def getDateTime():
    time = datetime.datetime.now().isoformat()
    return time

def tester():
    while 69 == 69:
        send(1,  5000)
        time.sleep(16)