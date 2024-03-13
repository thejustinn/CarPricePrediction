#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("..\src")


# In[2]:


# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/Users/smu/Downloads/Data-Science-Projects/Project_2_SgCarMart Price Prediction/src')
 


# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

from sgcarmart_webscraper_functions import * # Imports all defined webscraping functions


# # WebScraping

# In[3]:


# Creating a list of main pages to iterate through
main_page_listing_list = [] # creating list to store search pages of 100 car listings 
for idx, link in enumerate(range(166)):
    url = "https://www.sgcarmart.com/used_cars/listing.php?BRSR=" + str(idx * 100) + "&RPG=100&AVL=2&VEH=2"
    main_page_listing_list.append(url)


# In[4]:


print(main_page_listing_list,'\n','\n', len(main_page_listing_list))


# ## Retrieving individual listing urls from search pages of 100 listings

# In[5]:


# Base url, or you can think of this as the individual car listing prefix
base_url = 'https://www.sgcarmart.com/used_cars/'
listing_urls = []

# Acquiring indvidual car listings    
for main_link in main_page_listing_list:
   
    # Make a request to the website and get the object
    content = requests.get(main_link)

    # Parse the HTML text
    soup = BeautifulSoup(content.text, 'lxml')

    # Find every single URL in the webpage , refer to this post: # https://stackoverflow.com/questions/46490626/getting-all-links-from-a-page-beautiful-soup
    # This returns a list of every tag that contains a link in one main link (each element in main page listing)
    links = soup.find_all('a')
    
    # Create a list for storing all the individual listing urls
    
    for link in links:
        # Get link in <a href>
        suffix = link.get('href')

        # Check if 'ID=' and 'DL=' exist in the string
        if ('ID=' in suffix) and ('DL=' in suffix):

            # Concatenate the two strings if they do
            listing_url = base_url + suffix
            
            # Append result to the list
            listing_urls.append(listing_url)
            
#     Removing duplicates
    set_listing_urls = set(listing_urls)
    listing_urls = list(set_listing_urls)
    
    # Prevent oneself from getting blocked from the website
    time.sleep(1)


# In[6]:


print(len(listing_urls))
print(len(set(listing_urls)))
print(len(list(set(listing_urls))))


# In[7]:


print(listing_urls[:10])


# ## DataFrame Creation

# In[8]:


# Creating an empty DataFrame for attributes of interest
df = pd.DataFrame(columns=['LISTING_URL', 'BRAND', 'PRICE', 'DEPRE_VALUE_PER_YEAR',
       'REG_DATE', 'MILEAGE_KM', 'MANUFACTURED_YEAR',
       'ROAD_TAX_PER_YEAR','TRANSMISSION', 'DEREG_VALUE_FROM_SCRAPE_DATE',
       'SCRAPE_DATE', 'OMV', 'ARF', 'COE_FROM_SCRAPE_DATE',
       'DAYS_OF_COE_LEFT', 'ENGINE_CAPACITY_CC', 'CURB_WEIGHT_KG',
       'NO_OF_OWNERS', 'VEHICLE_TYPE','POST_DATE'])


# In[9]:


# Brand Retriever Function
def brand_retrieval(parsed_url):

    brand_name = parsed_url.find(class_='nounderline globaltitle').text.split()[0]
    return brand_name


# In[12]:


filename = 'sgcarmart_used_cars_prices7'
i = 0 # Indexing rows in the DF

for listingurl in listing_urls:
    response = requests.get(listingurl)
    listing_url = BeautifulSoup(response.text, 'lxml')
    
    # Retrieval functions to pull data from the Individual Listings after they have been parsed
    df.loc[i, 'LISTING_URL'] = listingurl
    
    try:
        df.loc[i, 'BRAND'] = brand_retrieval(listing_url)       
    except:
        df.loc[i, 'BRAND']= np.nan
    
    try:
        df.loc[i, 'PRICE'] = price_retrieval(listing_url)
    except:
        df.loc[i, 'PRICE']=np.nan
        
    try:
        df.loc[i, 'DEPRE_VALUE_PER_YEAR'] = depreciation_value_per_year_retrieval(listing_url)
    except:
        df.loc[i, 'DEPRE_VALUE_PER_YEAR'] = np.nan
        
    try:
        df.loc[i, 'REG_DATE'] = registered_date_retrieval(listing_url)
    except:
        df.loc[i, 'REG_DATE'] = np.nan
    
    try:
        df.loc[i, 'MILEAGE_KM'] = mileage_retrieval(listing_url)
    except:
        df.loc[i, 'MILEAGE_KM'] = np.nan

    try:
        df.loc[i, 'MANUFACTURED_YEAR'] = manufactured_year_retrieval(listing_url)
    except: 
        df.loc[i, 'MANUFACTURED_YEAR'] = np.nan
    
    try:
        df.loc[i, 'ROAD_TAX_PER_YEAR'] = road_tax_retrieval(listing_url)
    except:
        df.loc[i, 'ROAD_TAX_PER_YEAR'] = np.nan
        
    try:
        df.loc[i, 'TRANSMISSION'] = transmission_retrieval(listing_url)
    except:
        df.loc[i, 'TRANSMISSION'] = np.nan

        
    try:
        df.loc[i, 'DEREG_VALUE_FROM_SCRAPE_DATE'] = dereg_value_retrieval(listing_url)
    except: 
        df.loc[i, 'DEREG_VALUE_FROM_SCRAPE_DATE'] = np.nan
        
    df.loc[i, 'SCRAPE_DATE'] = datetime.now().strftime("%d/%m/%Y")
    
    try:
        df.loc[i, 'OMV'] = omv_retrieval(listing_url)
    except: 
        df.loc[i, 'OMV'] = np.nan

    try:
        df.loc[i, 'ARF'] = arf_retrieval(listing_url)
    except: 
        df.loc[i, 'ARF'] = np.nan
        
    try:
        df.loc[i, 'COE_FROM_SCRAPE_DATE'] = coe_retrieval(listing_url)
    except:
        df.loc[i, 'COE_FROM_SCRAPE_DATE'] = np.nan
        
    try:
        df.loc[i, 'DAYS_OF_COE_LEFT'] = days_of_coe_retrieval(listing_url)
    except:
        df.loc[i, 'DAYS_OF_COE_LEFT'] = np.nan
        
    try:
        df.loc[i, 'ENGINE_CAPACITY_CC'] = engine_capacity_retrieval(listing_url)
    except: 
        df.loc[i, 'ENGINE_CAPACITY_CC'] = np.nan
        
    try:
        df.loc[i, 'CURB_WEIGHT_KG'] = curb_weight_retrieval(listing_url)
    except:
        df.loc[i, 'CURB_WEIGHT_KG'] = np.nan
        
    try:
        df.loc[i, 'NO_OF_OWNERS'] = number_of_owners_retrieval(listing_url)
    except:
        df.loc[i, 'NO_OF_OWNERS'] = np.nan
        
    try:
        df.loc[i, 'VEHICLE_TYPE'] = type_of_vehicle_retrieval(listing_url)
    except:
        df.loc[i, 'VEHICLE_TYPE'] = np.nan
        
    try:
        df.loc[i, 'POST_DATE'] = postdate_retrieval(listing_url)
    
    except:
        df.loc[i, 'POST_DATE'] = np.nan

    print(i)
        
    df.to_csv("{}.csv".format(filename))    
        
    i += 1 # Allows next car listing to be put into a next row in the dataframe
    time.sleep(1)  # Prevents us from getting locked out of the website
    


# In[ ]:


df = pd.read_csv('sgcarmart_used_cars_prices3.csv',index_col=0)
df


# In[ ]:




