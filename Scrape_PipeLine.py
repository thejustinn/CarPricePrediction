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
        self.filename = 'sgcarmart_used_cars_prices_pipeline'
        self.base_url = "https://www.sgcarmart.com/used_cars/"

    def fetch_main_page(self):
        url = "https://www.sgcarmart.com/used_cars/listing.php?BRSR=0&RPG=100&AVL=2&VEH=2" 
        return url

    def fetch_listing_url(self, main_page_url):
        content = requests.get(main_page_url)
        soup = BeautifulSoup(content.text, 'lxml')
        print(soup)
        links = soup.find_all('a')
        print(links)
        for link in links:
            suffix = link.get('href')
            if ('ID=' in suffix) and ('DL=' in suffix):
                listing_url = self.base_url + suffix
                return listing_url  
        return None

    def brand_retrieval(self, parsed_url):
        try:
            return parsed_url.find(class_='nounderline globaltitle').text.split()[0]
        except:
            return np.nan

    def fetch_data(self, listing_url):
        response = requests.get(listing_url)
        data = {}
        data['LISTING_URL'] = listing_url
        data['SCRAPE_DATE'] = datetime.now().strftime("%d/%m/%Y")
        try:
            data['BRAND'] = self.brand_retrieval(listing_url)
        except:
            data['BRAND'] = np.nan
        try:
            data['PRICE'] = price_retrieval(listing_url)
        except:
            data['PRICE']=np.nan
            
        try:
            data['DEPRE_VALUE_PER_YEAR'] = depreciation_value_per_year_retrieval(listing_url)
        except:
            data['DEPRE_VALUE_PER_YEAR'] = np.nan
            
        try:
            data['REG_DATE'] = registered_date_retrieval(listing_url)
        except:
            data['REG_DATE'] = np.nan
        
        try:
            data['MILEAGE_KM'] = mileage_retrieval(listing_url)
        except:
            data['MILEAGE_KM'] = np.nan

        try:
            data['MANUFACTURED_YEAR'] = manufactured_year_retrieval(listing_url)
        except: 
            data['MANUFACTURED_YEAR'] = np.nan
        
        try:
            data['ROAD_TAX_PER_YEAR'] = road_tax_retrieval(listing_url)
        except:
            data['ROAD_TAX_PER_YEAR'] = np.nan
            
        try:
            data['TRANSMISSION'] = transmission_retrieval(listing_url)
        except:
            data['TRANSMISSION'] = np.nan

            
        try:
            data['DEREG_VALUE_FROM_SCRAPE_DATE'] = dereg_value_retrieval(listing_url)
        except: 
            data['DEREG_VALUE_FROM_SCRAPE_DATE'] = np.nan
            
        data['SCRAPE_DATE'] = datetime.now().strftime("%d/%m/%Y")
        
        try:
            data['OMV'] = omv_retrieval(listing_url)
        except: 
            data['OMV'] = np.nan

        try:
            data['ARF'] = arf_retrieval(listing_url)
        except: 
            data['ARF'] = np.nan
            
        try:
            data['COE_FROM_SCRAPE_DATE'] = coe_retrieval(listing_url)
        except:
            data['COE_FROM_SCRAPE_DATE'] = np.nan
            
        try:
            data['DAYS_OF_COE_LEFT'] = days_of_coe_retrieval(listing_url)
        except:
            data['DAYS_OF_COE_LEFT'] = np.nan
            
        try:
            data['ENGINE_CAPACITY_CC'] = engine_capacity_retrieval(listing_url)
        except: 
            data['ENGINE_CAPACITY_CC'] = np.nan
            
        try:
            data['CURB_WEIGHT_KG'] = curb_weight_retrieval(listing_url)
        except:
            data['CURB_WEIGHT_KG'] = np.nan
            
        try:
            data['NO_OF_OWNERS'] = number_of_owners_retrieval(listing_url)
        except:
            data['NO_OF_OWNERS'] = np.nan
            
        try:
            data['VEHICLE_TYPE'] = type_of_vehicle_retrieval(listing_url)
        except:
            data['VEHICLE_TYPE'] = np.nan
            
        try:
            data['POST_DATE'] = postdate_retrieval(listing_url)
        
        except:
            data['POST_DATE'] = np.nan
        
        return data

    # def run_pipeline(self):
        # main_page_url = self.fetch_main_page()
        # listing_url = self.fetch_listing_url(main_page_url)
        # if listing_url:
        #     data = self.fetch_data(listing_url)
        #     self.df = self.df.append(data, ignore_index=True)
        #     self.df.to_csv("{}.csv".format(self.filename))
        #     return self.df
        # else:
        #     print("No valid listing URL found.")
        #     return None

    def run_pipeline(self):
        main_page_url = self.fetch_main_page()
        print(main_page_url)
        listing_url = self.fetch_listing_url(main_page_url)
        print(listing_url)
        if listing_url:
            data = self.fetch_data(listing_url)
            self.df = self.df._append(data, ignore_index=True)
            self.df.to_csv("{}.csv".format(self.filename))
            return self.df
        else:
            print("No valid listing URL found.")
            return None

pipeline = Scrape_PipeLine()
pipeline.run_pipeline()
