from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

from sgcarmart_webscraper_functions import *  # Imports all defined webscraping functions

class Scrape_PipeLine:
    def __init__(self):
        self.df = pd.DataFrame(columns=['LISTING_URL', 'BRAND', 'PRICE', 'DEPRE_VALUE_PER_YEAR',
                                         'REG_DATE', 'MILEAGE_KM', 'MANUFACTURED_YEAR',
                                         'ROAD_TAX_PER_YEAR', 'TRANSMISSION', 'DEREG_VALUE_FROM_SCRAPE_DATE',
                                         'SCRAPE_DATE', 'OMV', 'ARF', 'COE_FROM_SCRAPE_DATE',
                                         'DAYS_OF_COE_LEFT', 'ENGINE_CAPACITY_CC', 'CURB_WEIGHT_KG',
                                         'NO_OF_OWNERS', 'VEHICLE_TYPE', 'POST_DATE'])
        self.filename = 'sgcarmart_used_cars_prices7'
        self.base_url = 'https://www.sgcarmart.com/used_cars/'

    def fetch_main_pages(self):
        main_page_listing_list = []
        for idx in range(166):
            url = "https://www.sgcarmart.com/used_cars/listing.php?BRSR=" + str(idx * 100) + "&RPG=100&AVL=2&VEH=2"
            main_page_listing_list.append(url)
        return main_page_listing_list

    def fetch_listing_urls(self, main_page_listing_list):
        listing_urls = []
        for main_link in main_page_listing_list:
            content = requests.get(main_link)
            soup = BeautifulSoup(content.text, 'lxml')
            links = soup.find_all('a')
            for link in links:
                suffix = link.get('href')
                if ('ID=' in suffix) and ('DL=' in suffix):
                    listing_url = self.base_url + suffix
                    listing_urls.append(listing_url)
            time.sleep(1)
        return list(set(listing_urls))

    def brand_retrieval(self, parsed_url):
        try:
            return parsed_url.find(class_='nounderline globaltitle').text.split()[0]
        except:
            return np.nan

    def fetch_data(self, listing_url):
        response = requests.get(listing_url)
        listing_url = BeautifulSoup(response.text, 'lxml')
        data = {}
        data['LISTING_URL'] = listing_url
        data['SCRAPE_DATE'] = datetime.now().strftime("%d/%m/%Y")
        try:
            data['BRAND'] = self.brand_retrieval(listing_url)
        except:
            data['BRAND'] = np.nan
        # Add other data retrieval logic here
        return data

    def run_pipeline(self):
        main_page_listing_list = self.fetch_main_pages()
        listing_urls = self.fetch_listing_urls(main_page_listing_list)
        for idx, listing_url in enumerate(listing_urls):
            data = self.fetch_data(listing_url)
            self.df = self.df.append(data, ignore_index=True)
            self.df.to_csv("{}.csv".format(self.filename))
            print(idx)
            time.sleep(1)
        return self.df

pipeline = Scrape_PipeLine()
pipeline.run_pipeline()
