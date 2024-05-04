from datetime import date
import itertools
import os
import pandas as pd
import multiprocessing
import concurrent.futures

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from . import helpers, selenium_scrape


class StoreScraper:

    def __init__(self, date_stamp=None):
        # initialize current date
        self.current_date = date.today()
        # initialize date stamp
        if date_stamp == None:
            self.date_stamp = (
                f"{self.current_date.year}{self.current_date.month}{self.current_date.day}"
            )
        else:
            self.date_stamp = date_stamp
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
        serv_obj = Service(DRIVER_PATH, service_args=["--log-level=INFO"])
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

    def get_product_csv_dict(self, scrape_date=None) -> dict:

        if scrape_date is None:
            scrape_date = self.date_stamp
        else:
            self.date_stamp = scrape_date

        # csv dictionary
        csv_dict = {}

        # define storage path
        for store in self.store_information_dict.keys():

            # get all the csvs of today
            product_urls_csv_path = (
                self.storage_path + f"{store}\\{scrape_date}\\{store}_product_urls"
            )

            # product csv list
            product_urls_csvs = os.listdir(product_urls_csv_path)
            # product csv list
            product_urls_csvs = [
                product_urls_csv_path + f"\\{file_name}"
                for file_name in product_urls_csvs
            ]
            # add list of csv to store key
            csv_dict[store] = product_urls_csvs

        return csv_dict

    # def get_product_data(self, csv_file_path):#name, store, scrape_date=None):
    #     # if scrape_date is None:
    #     #     scrape_date = self.date_stamp
    #     # define csv absolute path
    #     # product_csv_path = self.storage_path + f"{store}\\{scrape_date}\\_product_urls"
    #     # try to create a pandas dataframe
    #     try:
    #         product_df = pd.read_csv(csv_file_path)
    #     except Exception as e:
    #         print(f"{e} - could not read this file {csv_file_path}")
    #     # define output list to store dictionaries
    #     output_list_dicts = []
    #     # get the product category
    #     product_category = product_df["product_category"][0]
    #     # get the product information date
    #     product_info_date = product_df["product_info_date"][0]
    #     # loop through the product_urls to scrape products
    #     for product_link in product_df["product_urls"]:
    #         print(product_link)  # debugging
    #         # create the product dictionary
    #         product_dict = {}
    #         # set product category
    #         product_dict["category"] = product_category
    #         # set the date of product information
    #         product_dict["date"] = product_info_date
    #         # scrape with beautiful soup
    #         try:
    #             driver = self.driver
    #             # get the web page
    #             driver.get(product_link)
    #             # parse the web page with beautiful soup
    #             page_soup = BeautifulSoup(driver.page_source, "html.parser")
    #         except Exception as e:
    #             print(
    #                 f"{e} - could not create a beautiful soup object from the given link"
    #             )
    #         # get the product name
    #         product_name = page_soup.css.select(".prod-name")[0].getText()
    #         # get the product barcode
    #         product_barcode = (
    #             page_soup.find("li", string="Product code:")
    #             .find_next_sibling()
    #             .get_text()
    #         )
    #         # get the product price
    #         product_price = float(
    #             page_soup.css.select(f".prod--price")[0].getText().replace("R ", "")
    #         )
    #         # get the product weight
    #         product_weight = helpers.weight_extract_convert(product_name)

    #         product_dict["name"] = product_name
    #         product_dict["barcode"] = product_barcode
    #         product_dict["price"] = product_price
    #         product_dict["weight"] = product_weight
    #         product_dict["category"] = product_category
    #         product_dict["info_date"] = product_info_date
    #         product_dict["url"] = product_link

    #         # append to list
    #         output_list_dicts.append(product_dict)

    #     # return list of dictionaries
    #     return output_list_dicts

    def multiprocess_scrape(self, store, scrape_date, csv_list):
        if __name__ == "__main__":
            with concurrent.futures.ProcessPoolExecutor() as executor:
                scrape_results = [
                    executor.submit(
                        self.get_product_data,
                        args=[csv_list, store],
                        kwargs=[scrape_date],
                    )
                ]
                final_list = list(itertools.chain(scrape_results))

                # create output csv
                product_data_df = pd.DataFrame(final_list)
                # save to csv
                product_data_df.to_csv(
                    self.storage_path
                    + f"{store}\\{scrape_date}\\{store}_product_data\\products_data_{scrape_date}.csv",
                    index=False,
                )
        else:
            print("Not Executing")
