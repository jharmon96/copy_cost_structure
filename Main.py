from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time
import copy_cost_structure
import standard_functions
import settings
from pynput.keyboard import Controller

# Main.py kicks off the script


# initialize keyboard controller
settings.keyboard = Controller()

# initialize web browser used to retrieve / input information
standard_functions.initialize_browser()

# call the login function
standard_functions.login()

# Kick off process
copy_cost_structure.navigate()

# exit out of web browser
time.sleep(1)
settings.driver.quit()
