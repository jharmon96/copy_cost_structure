import csv
import os
from pynput.keyboard import Key
import time
import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

home = str(Path.home())


# starts google chrome in either headless (export) or standard (import) mode.

def initialize_browser():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\unanet_imu_CSV\Export Files"}
    chromeOptions.add_experimental_option("prefs", prefs)
    #chromeOptions.add_argument("--headless")
    chromeDriver = r"C:\unanet_imu_CSV\drivers\chromedriver.exe"
    settings.driver = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chromeOptions)


# logs into the browser with credentials provided in settings.py

def login():
    settings.driver.get(settings.URL + "/home")

    id_box = settings.driver.find_element_by_name('username')
    id_box.send_keys(settings.username)

    pass_box = settings.driver.find_element_by_name('password')
    pass_box.send_keys(settings.password)

    login_button = settings.driver.find_element_by_name('button_ok')
    login_button.click()

