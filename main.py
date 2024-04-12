import pprint
from datetime import date

from web_scrape import helpers, selenium_scrape


# get current date
current_date = date.today()
# extract day, month, and year from current_date
# day, month, year = current_date.day, current_date.month, current_date.year

# define date_stamp
date_stamp = f"{current_date.year}{current_date.month}{current_date.day}"


# get woolworths category information - category and url
store_information_dict = helpers.get_store_url_dict(r"Store_Category_Sheet.xlsx")

for store, category_dict in store_information_dict.items():
    # create directory
    helpers.create_directory(f"\\data\\stores\\{store}")
    for category, category_url in category_dict.items():
        category_products_links = selenium_scrape.url_scraper(category_url=category_url, category=category)
        print(category_products_links)
# pprint.pprint(helpers.get_store_url_dict(r"Store_Category_Sheet.xlsx"))
