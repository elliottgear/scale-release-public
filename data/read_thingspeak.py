#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################

import requests
import time
from redcap_writter import redcapRunner

'''
Reads data from thingspeak then invokes the readcap writter to write it to redcap.
This should be run 24/7 on a server since the Rpi is incapable of writting to Redcap,
or I could not figure out how to anyway.
'''
def main(old_id = 0):
    while True:
        latest_id = requests.get('https://api.thingspeak.com/channels/1331940/fields/1/last.txt')
        latest_id = latest_id.text
        if old_id != latest_id:
            print(old_id)
            print(latest_id)
            print('entering new data')
            # get all the info
            id = requests.get('https://api.thingspeak.com/channels/1331940/fields/1/last.txt')
            patientID = requests.get('https://api.thingspeak.com/channels/1331940/fields/2/last.txt')
            weight = requests.get('https://api.thingspeak.com/channels/1331940/fields/3/last.txt')
            date = requests.get('https://api.thingspeak.com/channels/1331940/fields/4/last.txt')

            # put it into redcap
            redcapRunner(id.text, weight.text, date.text)
            old_id = latest_id
        else:
            print("No new data, sleeping...")
        time.sleep(10)


if __name__ == "__main__":
    main()