from datetime import date
import os
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from . import helpers, selenium_scrape


class StoreScraper:

    def __init__(self):
        # initialize current date
        self.current_date = date.today()
        # initialize date stamp
        self.date_stamp = (
            f"{self.current_date.year}{self.current_date.month}{self.current_date.day}"
        )
        # initialize store category information
        self.store_information_dict = helpers.get_store_url_dict(
            r"Store_Category_Sheet.xlsx"
        )
        # initialize storage path
        self.storage_path = os.getcwd() + f"\\data\\stores\\"
        # CREATE DRIVER FOR SCRAPING DATA
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        DRIVER_PATH = os.getcwd() + r"\\web_scrape\\chromedriver.exe"
        serv_obj = Service(DRIVER_PATH)
        self.driver = webdriver.Chrome(service=serv_obj, options=options)

    def get_product_urls(self):
        # define date stamp
        date_stamp = self.date_stamp
        # get store category information

        store_information_dict = self.store_information_dict
        # create storage path

        storage_path = self.storage_path

        for store, category_dict in store_information_dict.items():
            # create directory for current date
            helpers.create_directory(storage_path + f"{store}\\{date_stamp}")
            for category, category_url in category_dict.items():
                # create directory to store product urls
                product_url_path = (
                    storage_path + f"{store}\\{date_stamp}\\{store}_product_urls"
                )
                helpers.create_directory(product_url_path)

                # create directory to store product data
                product_data_path = (
                    storage_path + f"{store}\\{date_stamp}\\{store}_product_data"
                )

                helpers.create_directory(product_data_path)

                # get scrape product urls

                category_product_links = selenium_scrape.url_scraper(
                    category_url=category_url, category=category
                )

                # sanitize category string to remove unwanted characters and whitespaces
                sanitized_category = helpers.sanitize_category(category)
                # write product urls to csv
                helpers.create_product_urls_csv(
                    category_product_links,
                    sanitized_category,
                    self.current_date,
                    product_url_path,
                )

    def get_product_data(self):

        # define storage path
        for store in self.store_information_dict.keys():
            # get all the csvs of today
            product_urls_csv_path = (
                self.storage_path + f"{store}\\{self.date_stamp}\\{store}_product_urls"
            )
            # print(os.listdir(product_urls_csv_path))

            # product csv list
            product_urls_csvs = os.listdir(product_urls_csv_path)
            # create list to store dictionaries
            output_dict_list = []
            for product_url_csv in product_urls_csvs:
                try:
                    product_df = pd.read_csv(
                        product_urls_csv_path + f"\\{product_url_csv}"
                    )
                except Exception as e:
                    continue
                else:
                    # get links from product_df
                    product_links = product_df["product_urls"]
                    for product_link in product_df["product_urls"]:
                        # create product dictionary
                        product_dict = {}
                        # set product category
                        product_dict["category"] = product_df["product_category"][0]
                        # set date of product information
                        product_dict["date"] = product_df["product_info_date"]
                        try:
                            driver = self.driver
                            driver.get(product_link)
                            page_soup = BeautifulSoup(driver.page_source, "html.parser")

                            # get product name
                            product_name = page_soup.css.select("prod-name")[
                                0
                            ].getText()
                            # get product barcode
                            product_barcode = (
                                page_soup.find("li", string="Product code:")
                                .find_next_sibling()
                                .get_text()
                            )
                            # get product price
                            price_id = f"price_{product_barcode}_{product_barcode}"
                            product_price = float(
                                page_soup.css.select(f".prod--price")[0]
                                .getText()
                                .replace("R ", "")
                            )
                            # get product weight
                            product_weight = helpers.weight_extract_convert(
                                product_name
                            )

                            product_dict["name"] = product_name
                            product_dict["barcode"] = product_barcode
                            product_dict["price"] = product_price
                            product_dict["weight"] = product_weight
                            output_dict_list.append(product_dict)

                        except Exception as e:
                            print(e)

            # convert output_dict to pandas
            product_data_df = pd.DataFrame(output_dict_list)
            # save to csv
            product_data_df.to_csv(self.storage_path + f"{store}\\{self.date_stamp}\\{store}_product_data\\products_data_{self.date_stamp}.csv", index=False)
            print("data saved")
