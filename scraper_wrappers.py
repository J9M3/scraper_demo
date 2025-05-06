from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random


def next_page_clicker(by , element , my_driver):
    next_button = my_driver.find_element(by = by , value = element )
    time.sleep(random.uniform(1.5, 3.0))
    my_driver.execute_script("arguments[0].scrollIntoView();", next_button)
    my_driver.execute_script("arguments[0].click();", next_button)


def standard_currecy_converter(input):
    if pd.isna(input):
        return pd.NA
    else:
        input = input.replace( "£" , "")
        input = input.replace("," , "")
        input = input.split(".")[0]
        input = int(input)
        return input