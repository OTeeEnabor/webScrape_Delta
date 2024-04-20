import os
import pprint
from datetime import date

from web_scrape import helpers, selenium_scrape

# get current date
current_date = date.today()

# define date_stamp
date_stamp = f"{current_date.year}{current_date.month}{current_date.day}"

# get woolworths category information - category and url
store_information_dict = helpers.get_store_url_dict(r"Store_Category_Sheet.xlsx")

# create storage path
storage_path = os.getcwd() + f"\\data\\stores\\"

for store, category_dict in store_information_dict.items():
    
    # create directory
    helpers.create_directory(storage_path+f"{store}\\{date_stamp}")

    for category, category_url in category_dict.items():
        # create directory to store product urls
        product_url_path = storage_path+f"{store}\\{date_stamp}\\{store}_product_urls"

        helpers.create_directory(product_url_path)
        # get scrape product urls
        category_products_links = selenium_scrape.url_scraper(category_url=category_url, category=category)
        
        # sanitize category string to remove unwanted characters and whitespaces
        sanitized_category = helpers.sanitize_category(category)
        # write product urls to csv
        helpers.create_product_urls_csv(category_products_links, sanitized_category, current_date, product_url_path)
# pprint.pprint(helpers.get_store_url_dict(r"Store_Category_Sheet.xlsx"))
