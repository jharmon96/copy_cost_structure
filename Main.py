from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import time
import cost_structure
import standard_functions
import user_input
import settings
from pynput.keyboard import Controller

# Main.py kicks off the script

user_input.prompt_credentials()
user_input.prompt_direction()
user_input.prompt_details()


# initialize keyboard controller
settings.keyboard = Controller()

# call the login function
standard_functions.login()

# Kick off process
cost_structure.run()

# Test #
# export_cost_structure.test()


# exit out of web browser
time.sleep(1)
settings.driver.quit()
