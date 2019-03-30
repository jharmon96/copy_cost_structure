import settings
import standard_functions
from pynput.keyboard import Key
import time

# Navigates to the proper pages where changes are to be made, then kicks off the process

def navigate():
    # Navigates to cost structure list URL

    webPage = settings.URL + "/admin/setup/project/cost_structures/list"
    settings.driver.get(webPage)
    xpathId = '//*[@id="body"]/div/div[2]/table/tbody/tr[1]/td/a'
    settings.driver.find_element_by_xpath(xpathId).click()
    create()

def create():

   Summary()
   Labor_Costs()

def Summary():
    # Name cost structure
    input_value = "test"
    xpathId = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[1]/td[2]/input'
    settings.driver.find_element_by_xpath(xpathId).send_keys(input_value)
    Save()
    time.sleep(1)

def Labor_Costs():
    # navigate to Labor Cost Elements
    xpathId = '//*[@id="tab.costing.labor_head"]/span'
    settings.driver.find_element_by_xpath(xpathId).click()
    time.sleep(1)
    left_to_right()
    left_to_right()
    left_to_right()
    Save()


def ODC_Costs():
    pass

def Indirect_Costs():
    pass

def Indirect_Cost_Rates():
    pass

def left_to_right():
    # select left hand value
    xpathId = '//*[@id="tab.costing.labor"]/form/div[2]/table/tbody/tr[2]/td[1]/select/option[1]'
    settings.driver.find_element_by_xpath(xpathId).click()
    # add left hand value to right column
    xpathId = '//*[@id="tab.costing.labor"]/form/div[2]/table/tbody/tr[2]/td[2]/img[2]'
    settings.driver.find_element_by_xpath(xpathId).click()

def Save():
    # Save new new Labor Cost Elements
    xpathId = '//*[@id="button_save"]'
    settings.driver.find_element_by_xpath(xpathId).click()
