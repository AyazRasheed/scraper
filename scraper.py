import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd
import time

# Configure Selenium to run in headless mode
def driver_init():
    options = uc.ChromeOptions()  # Use the correct ChromeOptions from undetected_chromedriver
    download_dir = "/content/drive/My Drive/Downloads"  # Change to your desired folder in Google Drive
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "profile.default_content_settings.popups": 0,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--disable-blink-features=AutomationControlled')  # Reduce automation detection
    options.add_argument('--window-size=1920,1080')  # Set window size for screenshots
    # options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36')

    # Initialize the undetected_chromedriver with options
    driver = uc.Chrome(options=options)
    return driver

df = pd.read_excel("my_zips_data.xlsx")



driver = driver_init()
for index, row in df[df['data'].isna()].iterrows():
    zip_code = row['zip']
    city = row['city']
    state_id = row['state_id']
    if len(str(zip_code))<5:
        zip_code = '0'+str(zip_code)
    time.sleep(1)
    inp_str = f"{city}, {zip_code} {state_id}, USA"
#     driver.get("https://riflepaperco.com/pages/store-locator")
    inp_area = driver.find_element(By.XPATH, '//input[@class="stockist-search-field pac-target-input"]')
    inp_area.clear()
    inp_area.send_keys(inp_str)
    time.sleep(0.5)
    inp_area.send_keys(Keys.ENTER)
    time.sleep(1.5)
    results = []
    for stockist in driver.find_elements(By.XPATH, '//div[@class="stockist-result-list"]//li'):
        try:
            distance = stockist.find_element(By.XPATH, ".//span[contains(@class, 'stockist-result-distance-text')]").text
        except:
            distance = ""

        try:
            name = stockist.find_element(By.XPATH, ".//div[contains(@class, 'stockist-result-name')]").text
        except:
            name = ""

        try:
            address_1 = stockist.find_element(By.XPATH, ".//div[contains(@class, 'stockist-result-addr-1')]").text
        except:
            address_1 = ""

        try:
            locality = stockist.find_element(By.XPATH, ".//div[contains(@class, 'stockist-result-addr-locality')]").text
        except:
            locality = ""

        try:
            country = stockist.find_element(By.XPATH, ".//div[contains(@class, 'stockist-result-addr-country')]").text
        except:
            country = ""

        try:
            directions_link = stockist.find_element(By.XPATH, ".//div[contains(@class, 'stockist-result-directions-link')]/a").get_attribute("href")
        except:
            directions_link = ""
        dict_data = {
            "Distance": distance,
            "Name": name,
            "Address 1": address_1,
            "Locality": locality,
            "Country":country,
            "Directions Link": directions_link,
            }
        results.append(dict_data)
        df.at[index, "data"] = str(results)
        print(index, '\n')
        if index%10==0:
            print(index, all_data)
            df.to_excel('results.xlsx', index=False)
