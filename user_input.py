import settings
import time


# Ask for login info
def prompt_credentials():
    settings.URL = input("What is the URL? \nExample: 'http://sites.unanet.com/demo'\n")
    settings.username = input("Enter the username: ")
    settings.password = input("Enter the password: ")


# Ensures the end user types 'Import', 'Export', or 'Copy'
def prompt_direction():
    ask_again = True

    while ask_again:
        settings.direction = input("Would you like to Export, Import, or Copy? ")
        ask_again = False
        if settings.direction == "Export" or settings.direction == "Import" or settings.direction == "Copy":
            break
        else:
            ask_again = True
            print("Please choose Export, Import, or Copy")
            time.sleep(1)


#############################################################################################
### Prompt Details ##########################################################################
#############################################################################################
def cs_export():
    settings.cost_structure = input("Which cost structure would you like to export? ")


def cs_import():
    pass


def cs_copy():
    settings.cost_structure = input("Which cost structure would you like to copy? ")
    settings.new_cost_structure = input("What would you like to name the new cost structure? ")


options = {"Export": cs_export,
           "Import": cs_import,
           "Copy": cs_copy
           }


def prompt_details():
    options[settings.direction]()

#############################################################################################
#############################################################################################
#############################################################################################
