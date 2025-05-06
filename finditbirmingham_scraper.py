from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import datetime
from scraper_wrappers import next_page_clicker , standard_currecy_converter

# Initialize the browser
driver = webdriver.Firefox()
base_url = "https://www.finditinbirmingham.com/opportunities"
driver.get(base_url)
data = []
source_id = "FIBM"


# Bypass cookies 

decline_cookies = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "ccc-reject-settings"))
    )

time.sleep(random.uniform(1.2, 3.0))

decline_cookies.click()

# Find Talbe 
table = driver.find_element(By.ID , "tblOpportunities")
table_elements = driver.find_elements(By.CLASS_NAME, "article-grid")

# Scrape data 

next_button_status = driver.find_element(By.ID , "tblOpportunities_next").get_attribute("class")



while next_button_status == 'paginate_button next':

    table = driver.find_element(By.ID , "tblOpportunities")
    table_elements = driver.find_elements(By.CLASS_NAME, "article-grid")
    
    for element in table_elements:

        tmp_dict = {"Tender_name" : element.find_element(By.CLASS_NAME , "row").text}

        element_key = element.find_elements(By.CLASS_NAME , "subheader")
        element_value = element.find_elements(By.CLASS_NAME , "text")
        cont_lenght = len(element_key) 
        
        for i in range(0 , cont_lenght):
            tmp_dict.update({element_key[i].text : element_value[i].text})

        if cont_lenght == 3:
            tmp_dict.update({"Value" : pd.NA})

        data.append(tmp_dict)

    next_button_status = driver.find_element(By.ID , "tblOpportunities_next").get_attribute("class")
    next_page_clicker(by = By.ID , element = "tblOpportunities_next" , my_driver = driver)

driver.close()

scrape_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define DF

df = pd.DataFrame(data)
#df = df.dropna().copy()

# Output CSV 

df["Closing Date"] = pd.to_datetime(df["Closing Date"] , format="%d/%m/%Y %H:%M") 
df["expiry_date"] = df["Closing Date"].dt.date
df["expiry_time"] = df["Closing Date"].dt.time
df= df.drop("Closing Date" , axis= 1 ).copy()

df["source_id"] = source_id
df["scraped_datetime"] = scrape_timestamp

df = df.rename(columns={
    "Value" : "tender_value" ,
    "Process" : "tendor_process",
    "Posted By" : "tender_issuer",
    "Location" : "location"
    })

df["tender_value"] = df["tender_value"].apply(standard_currecy_converter)

df.to_csv("Scraped_data/scraped_data_finditbirmingham.csv", header=True )


