#########################
# * Written by Elliott Gear for University of Vermont Senior Design
# * Spring 2021
# * SEED Team #9: WiFi Enhanced Electronic Scale Project
# * https://www.uvm.edu/cems/seed
# * egear@uvm.edu
# * MIT license, all text above must be included in any redistribution
#########################
'''
DOWNLOAD CHROME DRIVER and change the chromedriver_location variable to its locaition
Chrome Driver version must match that of chrome instaled on your system as well as OS.
64 bit only.
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#TODO make this object based to run more quickly without making a new object every time

# Setup function
""" Creates a chromedriver object, and calls the driver
Parameters
----------
id : string
    Patient ID number.
date : string
    date and time of the reading
weight : long
    Patient weight in KG
"""
def redcapRunner(id, date, weight):
    global driver

    # update for RPI location
    chromedriver_location = "/Users/egear/Downloads/chromedriver"

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chromedriver_location,options=chrome_options)
    driver.get('https://redcap.med.uvm.edu/surveys/?s=MXK97T7RNK')

    firstPage(id, date, weight)

""" Uses chrome driver and selenium to enter data into redcap
Parameters
----------
id : string
    Patient ID number.
date : string
    date and time of the reading
weight : long
    Patient weight in KG
"""
# main driver function to fill in feilds based on xpath data
def firstPage(id, date, weight):
    # xpath of the feilds we care about
    idField = '//*[@id="id-tr"]/td[3]/input'
    dateField = '//*[@id="date-tr"]/td[3]/input'
    weightField = '//*[@id="weight-tr"]/td[3]/input'
    submitButton = '//*[@id="questiontable"]/tbody/tr[4]/td/table/tbody/tr/td/button'

    # enter the patient id number
    driver.find_element_by_xpath(idField).send_keys(id)
    print("entering id number")
    time.sleep(.5)

    # enter the date
    driver.find_element_by_xpath(dateField).send_keys(date)
    print("entering date")
    time.sleep(.5)

    # enter the weight
    driver.find_element_by_xpath(weightField).send_keys(weight)
    print("entering weight")
    time.sleep(.5)

    # slap that next button
    driver.find_element_by_xpath(submitButton).click()

    print("data submitted")

