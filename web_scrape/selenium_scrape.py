import time
import re
import json
import logging
import os
from datetime import date

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from . import helpers

def create_driver():
    # initialise the webdriver
    options = webdriver.ChromeOptions()
    # set the mode to headless
    options.add_argument("--headless")
    # define the path of the driver
    DRIVER_PATH = os.getcwd() + r"\\web_scrape\\chromedriver.exe"
    # define the service object
    serv_obj = Service(DRIVER_PATH, service_args=["--log-level=INFO"])
    # create selenium driver
    driver = webdriver.Chrome(service=serv_obj, options=options)
    return driver


def url_scraper(category_url: str, category: str) -> list:

    # define Selenium Driver Path
    # print(os.getcwd())
    DRIVER_PATH = os.getcwd() + r"\\web_scrape\\chromedriver.exe"

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
    next_page_button = driver.find_elements(By.CLASS_NAME, "pagination__nav")[
        1
    ]  # second one because there could be the previous button, which has the same class name

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
                next_page_button = driver.find_elements(
                    By.CLASS_NAME, "pagination__nav"
                )
                # check if there is more than one button found
                if len(next_page_button) > 1:
                    next_page_button = next_page_button[1]
                    # scroll to the button
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", next_page_button
                    )
                    # click on button
                    next_page_button.click()
                else:
                    next_page_button = next_page_button[0]
                driver.implicitly_wait(10)
            except Exception as e:
                break
    return product_link_list


def get_product_data(csv_file_path):
    # initialise driver object
    sel_driver = create_driver()
    try:
        product_df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"{e} - could not read this file {csv_file_path}")
    # define output list to store dictionaries
    output_list_dicts = []
    # get the product category
    product_category = product_df["product_category"][0]
    # get the product information date
    product_info_date = product_df["product_info_date"][0]
    # loop through the product_urls to scrape products
    for product_link in product_df["product_urls"][:100]:
        print(product_link)  # debugging
        # create the product dictionary
        product_dict = {}
        # set product category
        product_dict["category"] = product_category
        # set the date of product information
        product_dict["date"] = product_info_date
        # scrape with beautiful soup
        try:
            # get the web page
            sel_driver.get(product_link)
            # parse the web page with beautiful soup
            page_soup = BeautifulSoup(sel_driver.page_source, "html.parser")
        except Exception as e:
            print(f"{e} - could not create a beautiful soup object from the given link")
        try:
            # get the product name
            product_name = page_soup.css.select(".prod-name")[0].getText()
        except IndexError as error:
            product_name = "error"
            print(f"could not get product name for {product_link}:error--{error}")
        except Exception as error:
            print(f"could not get product name for {product_link}:error--{error}")
            product_name = "error"
        # get the product barcode
        try:

            product_barcode = (
                page_soup.find("li", string="Product code:").find_next_sibling().get_text()
            )
        except Exception as error:
            product_barcode = "error"
            print(f"could not get product name for {product_link}:error--{error}")

        try:

            # get the product price
            product_price = float(
                page_soup.css.select(f".prod--price")[0].getText().replace("R ", "")
            )
        except Exception as error:
            product_price = "error"
            print(f"could not get product name for {product_link}:error--{error}")

        try:

            # get the product weight
            product_weight = helpers.weight_extract_convert(product_name)
        except Exception as error:
            product_weight = "error"
            print(f"could not get product name for {product_link}:error--{error}")

        product_dict["name"] = product_name
        product_dict["barcode"] = product_barcode
        product_dict["price"] = product_price
        product_dict["weight"] = product_weight
        product_dict["category"] = product_category
        product_dict["info_date"] = product_info_date
        product_dict["url"] = product_link

        # append to list
        output_list_dicts.append(product_dict)

    # return list of dictionaries
    return output_list_dicts
