import itertools
import os
import pprint
from datetime import date
import concurrent.futures
import time

import numpy as np
import pandas as pd
from web_scrape import helpers, selenium_scrape, store_scrape
from web_scrape.selenium_scrape import get_product_data

start = time.perf_counter()

# # initialise store scraper
store_scraper = store_scrape.StoreScraper(date_stamp="2024426")
print(store_scraper.date_stamp)
# get the url csvs
product_url_dict = store_scraper.get_product_csv_dict(
    scrape_date="2024426"
)  # get_product_urls()

for store, csv_list in product_url_dict.items():
    if __name__ == "__main__":
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(get_product_data, csv_list)
            output_list = []
            for result in results:
                list_result = list(result)
                print(list_result)
                output_list.append(list_result)
        results = list(np.concatenate(output_list).flat)
        # create output csv
        product_data_df = pd.DataFrame(results)
        print(product_data_df.head())
        # # save to csv
        product_data_df.to_csv(
            store_scraper.storage_path
            + f"{store}\\{store_scraper.date_stamp}\\{store}_product_data\\products_data_{store_scraper.date_stamp}.csv",
            index=False,
        )

finish = time.perf_counter()

print(f"finished in {round(finish-start,2)} seconds (s)")
