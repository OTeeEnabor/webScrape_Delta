import os
import pprint
import re
from datetime import date

import pandas as pd


def get_store_url_dict(spreadsheet_name: str) -> dict:
    """
    Return dictionary that contains product categories as keys and their URLS as values.

    param: sheet_path: the path to that contains category and URL information from each store.

    returns:
    category_dict: dictionary containing product categories as keys and their urls

    """

    # define data path
    file_path = r"data/" + f"{spreadsheet_name}"

    # load all sheets in the spreadsheet with pandas
    store_urls_df = pd.read_excel(file_path, sheet_name=None)

    # iterate through each sheet
    for store, store_df in store_urls_df.items():
        # set the Categories as the index
        store_df = store_df.set_index("Categories")
        # convert the store_df to dictionary with Categories as Key and URLs as value
        store_df_dict = store_df.to_dict()["URLs"]
        # store each converted dict as a value and use the store as a key
        store_urls_df[store] = store_df_dict
    return store_urls_df


def create_directory(path):
    """
    # create directory to store urls and logging file

    :param path: directory path where files will be stored.

    """
    # get current date
    today = date.today()
    # create folder name to store url and log files
    date_folder = f"{today.year}{today.month}{today.day}"

    # get directory path for url and log files  folder
    folder_path = f"{path}\\{date_folder}"

    current_dir = os.getcwd()
    folder_path = current_dir+folder_path

    # check if folder has already been created
    is_exists = os.path.exists(folder_path)
    # if created
    if is_exists:
        # print exists - will be removed
        print("exists")
    else:
        # if does not exits, create the folder
        # current_dir = os.getcwd()
        # folder_path = current_dir+folder_path
        # print(folder_path)
        os.makedirs(folder_path)
        # print folder created - will be removed
        print(f"{folder_path} created")
