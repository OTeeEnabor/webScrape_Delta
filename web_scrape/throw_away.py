"""
This python code are not being used at the moment. However, I do not want to throw them away just yet
"""

def get_product_data(self, date=None):
        if date is None:
            date = self.date_stamp
        # define storage path
        for store in self.store_information_dict.keys():
            # get all the csvs of today
            product_urls_csv_path = (
                self.storage_path + f"{store}\\{date}\\{store}_product_urls"
            )
            # print(os.listdir(product_urls_csv_path))

            # product csv list
            product_urls_csvs = os.listdir(product_urls_csv_path)
            # create list to store dictionaries
            output_dict_list = []
            for product_url_csv in product_urls_csvs[0:1]:
                try:
                    # create file path
                    product_file_path = product_urls_csv_path + f"\\{product_url_csv}"
                    product_df = pd.read_csv(product_file_path)
                except Exception as e:
                    print(
                        f"{e} - could not create a data frame using the path given - {product_file_path}"
                    )
                else:
                    # get the product category
                    product_category = product_df["product_category"][0]
                    # get the product information date
                    product_info_date = product_df["product_info_date"][0]
                    for product_link in product_df["product_urls"]:
                        print(product_link)
                        # create product dictionary
                        product_dict = {}
                        # set product category
                        product_dict["category"] = product_category
                        # set date of product information
                        product_dict["date"] = product_info_date
                        try:
                            driver = self.driver
                            driver.get(product_link)
                            page_soup = BeautifulSoup(driver.page_source, "html.parser")
                        except Exception as e:
                            print(
                                
                            )
                            # get product name
                            product_name = page_soup.css.select(".prod-name")[
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
                            print(product_dict)
                            output_dict_list.append(product_dict)

            # convert output_dict to pandas
            product_data_df = pd.DataFrame(output_dict_list)
            # save to csv
            product_data_df.to_csv(
                self.storage_path
                + f"{store}\\{date}\\{store}_product_data\\products_data_{date}.csv",
                index=False,
            )
            print("data saved")
