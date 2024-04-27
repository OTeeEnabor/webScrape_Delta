import os
import pprint
from datetime import date

from web_scrape import helpers, selenium_scrape, store_scrape


store_scraper = store_scrape.StoreScraper()

store_scraper.get_product_data()  # get_product_urls()


