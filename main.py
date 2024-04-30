import os
import pprint
from datetime import date

from web_scrape import helpers, selenium_scrape, store_scrape


store_scraper = store_scrape.StoreScraper()

# # get current date
# store_scraper.current_date
# # get store information dictionary
# print(store_scraper.store_information_dict)
# # print the driver object
# print(store_scraper.driver)

print(store_scraper.get_product_csv_list(date="2024426"))  # get_product_urls()
