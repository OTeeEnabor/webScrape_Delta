import time
import re
import json
import logging
import os
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 

def url_scraper(category_url:str, category:str) -> list:

    # define Selenium Driver Path
    # print(os.getcwd())
    DRIVER_PATH = os.getcwd()+r"\\web_scrape\\chromedriver.exe"

    # print(DRIVER_PATH)
    # create service object
    serv_obj = Service(DRIVER_PATH) 

    # instantiate selenium driver with service object
    driver = webdriver.Chrome(service=serv_obj)
    # implicit wait
    driver.implicitly_wait(0.5)
    # maximise the browser window
    driver.maximize_window()
    # get the html of category url
    driver.get(category_url)
    # wait for 5 seconds to load
    time.sleep(5)

    # look for each product URL in this category

    # find page next button
    next_page_button = driver.find_elements(By.CLASS_NAME,"pagination__nav")[1] # second one because there could be the previous button, which has the same class name

    # check if the button is on the page
    if next_page_button.is_displayed():
        # sleep for 5 seconds  - why?
        time.sleep(5)
        # create an empty list to store product links
        product_link_list = []

        while True:
            try:
                # find all anchor tags with the class - product--view
                product_anchors = driver.find_elements(By.CLASS_NAME, "product--view")

                for anchor in product_anchors:
                    # get the url
                    product_link = anchor.get_attribute("href")
                    # append the URL to the product link to the list of product links
                    product_link_list.append(product_link)
                
                # find the next_page_button again
                next_page_button = driver.find_elements(By.CLASS_NAME, "pagination__nav")
                # check if there is more than one button found
                if len(next_page_button) > 1 :
                    next_page_button  = next_page_button[1]
                    # scroll to the button
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                    # click on button
                    next_page_button.click()
                else:
                    next_page_button = next_page_button[0]
                driver.implicitly_wait(10)
            except Exception as e:
                break
    return product_link_list

