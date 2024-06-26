import os
import pprint
import re
from datetime import date

import pandas as pd


def sanitize_category(raw_category:str) -> str:
    """
    Transforms string to suitable category
    
    param: raw_category: string that is not suitable to use as category.

    returns
    clean_category: string suitable for use as a category. 
    """
    # remove whitespaces
    white_space_pattern = r'\s'

    clean_category = re.sub(white_space_pattern,"",raw_category)

    # define unwanted characters
    unwanted_characters = '[&,]'
    
    clean_category = re.sub(unwanted_characters,"_",clean_category)
    
    

    return clean_category

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


def create_directory(path) -> None:
    """
    create directory to store urls and logging file

    :param path: directory path where files will be stored.

    """
    
    # check if folder has already been created
    is_exists = os.path.exists(path)
    # if created
    if is_exists:
        # print exists - will be removed
        print("exists")
    else:
        # if does not exits, create the folder
        
        os.makedirs(path)
        # print folder created - will be removed
        print(f"{path} created")

def create_product_urls_csv(product_urls_list:list, product_category:str, current_date:str, store_path:str):
    """
    create a csv file containing product urls

    param: product_urls_list: a list of product urls scrapped from online store
    param: product_category: category for which all the product urls belong to
    param: current_date: date when urls were scrapped from internet and saved to the csv
    param: store: name of the store

    returns: product_urls_csv: csv file containing the product_urls
    """

    # create dictionary to store product url 
    product_dict = {
        "product_urls": product_urls_list,
        "product_category": product_category,
        "product_info_date": current_date
    }

    # convert dictionary to pandas dataframe
    product_urls_df = pd.DataFrame(product_dict)

    # write pandas dataframe to dataframe
    product_urls_df.to_csv(f"{store_path}\\{product_category}.csv",index=False)
    # give confirmation product_urls saved
    print(f"{store_path}\\{product_category}.csv  saved")

def create_product_data_directory():
    """
    Creates a directory to store the product scraped for that iteration
    """
    pass

def weight_extract_convert(weight_string):
    # combination regular expression
    combination_weight_re = "[0-9]+ x [0-9]+ (g|kg|ml|L)|[0-9]+ x [0-9]+.[0-9]+ (g|kg|ml|L)|[0-9]+x[0-9]+.[0-9]+ (g|kg|ml|L)|[0-9]+x[0-9]+(g|kg|ml|L)"
    # singular regular expression
    singular_weight_re = "[0-9]+ (g|kg|ml|L)|[0-9]+(g|kg|ml|L)"

    # check for combination string
    if re.search(combination_weight_re, weight_string):
        # split the string into list - [num units , weigh_per_unit]
        combination_split = (
            re.search(combination_weight_re, weight_string).group().split(" x ")
        )
        # num_units
        num_units = int(combination_split[0])
        # unit_string - [g,kg,ml, l]
        weight_unit_string = combination_split[1]
        # check if weight unit is grammes
        if " g" in weight_unit_string:
            # remove the gramme unit, convert string to float
            weight = float(weight_unit_string.replace(" g", ""))
            # divide weight by 1000 to convert to kg
            weight = weight / 1000 * num_units
        # check if weight unit is mil litres
        elif " ml" in weight_unit_string:
            # remove the ml unit, convert string to float
            weight = float(weight_unit_string.replace(" ml", ""))
            # divide wight by 1000 to L - 1l -kg
            weight = weight / 1000 * num_units
        # check if kg unit in string
        elif " kg" in weight_unit_string:
            # remove the kg unit in string, convert string to float
            weight = float(weight_unit_string.replace(" kg", "")) * num_units
        else:
            # remove L unit in string, convert string to float
            weight = float(weight_unit_string.replace(" L", "")) * num_units

    elif re.search(singular_weight_re, weight_string):
        # singular algorithm
        weight_string_singular = re.search(singular_weight_re, weight_string).group()
        if " g" in weight_string_singular:
            weight = float(weight_string_singular.replace(" g", "")) / 1000
        elif " ml" in weight_string_singular:
            weight = float(weight_string_singular.replace(" ml", "")) / 1000
        elif " kg" in weight_string_singular:
            weight = float(weight_string_singular.replace(" kg", ""))
        else:
            weight = float(weight_string_singular.replace(" L", ""))
    else:
        weight = None
    try:
        return round(weight, 2)
    except:
        return None