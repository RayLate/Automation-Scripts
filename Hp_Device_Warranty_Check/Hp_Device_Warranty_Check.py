from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pandas import DataFrame, Series

# ------------------------------------------------------------
# Excel file format
# SerialNum
# 4CE0290VK4
# 4CE0290VK8
# 4CE0290VKB
# 4CE0290VKD
# 4CE0290VKJ
# 4CE0290VKL
# 4CE0290VKP
# 4CE0290VKQ
# 4CE0290VL0


path = " " # location of the excel file containing device serial numbers

x1 = pd.read_excel(path)

# HP device serial number is 10 letters, remove serial number that is not 10 letters
snlist = x1[x1.SerialNum.str.len() == 10]

#Serial Number Series
SN = snlist['SerialNum']

print("Number of Hostname to check = {}".format(SN.size))

warranty =[]

# open chrome browser and navigate to web page.
driver = webdriver.Chrome()

for serialnumber in SN:
	print("Hostname Remaining = {}".format(SN.size-len(warranty)))
    driver.get("https://support.hp.com/sg-en/checkwarranty")

    # Find SN input field, if fail reopen chrome brower and try again
    try:
        SNfield = driver.find_element_by_xpath("//input[@id='wFormSerialNumber']")
    except expression as identifier:
        driver.close()
        driver = webdriver.Chrome()
        SNfield = driver.find_element_by_xpath("//input[@id='wFormSerialNumber']")

    SNfield.clear()
    SNfield.send_keys(serialnumber)
    checkwarranty = driver.find_element_by_xpath("//*[@id='btnWFormSubmit']")
    checkwarranty.click()

    # give browser 20 seconds to find the startdate and enddate element
    driver.implicitly_wait(20)
    try:
        # Base Warranty Start Date
        startdate = driver.find_element_by_xpath(
            "//*[@id='warrantyResultBase']/div/div[1]/div[1]/div[4]/div[2]")

        # Extended Warranty Start Date
        if not bool(startdate.text):
            startdate = driver.find_element_by_xpath(
                "//*[@id='additionalExtWarranty_1']/div/div/div[1]/div[4]/div[2]")
        startdate = startdate.text
    except:
        startdate = 'error'
    try:
        # Base Warranty End Date
        enddate = driver.find_element_by_xpath(
            "//*[@id='warrantyResultBase']/div/div[1]/div[1]/div[5]/div[2]")
        if not bool(enddate.text):
            # Extended Warranty End Date
            enddate = driver.find_element_by_xpath(
                "//*[@id='additionalExtWarranty_1']/div/div/div[1]/div[5]/div[2]")

        enddate = enddate.text
    except:
        enddate ='error'

    devicewarranty = [serialnumber,startdate,enddate]
    print(devicewarranty)
    warranty.append(devicewarranty)

warrantydf = DataFrame(warranty,columns=['Serial_Number','startdate','enddate'])

# outout warranty date file
warrantydf.to_csv(r"{}\warranty.csv".format(path),index=False)

driver.close()
