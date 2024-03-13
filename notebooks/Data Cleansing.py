#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# Our project aims to identify an optimal pricing model using regression techniques to quantify what the reasonable price range of a car would be, which Atlas Motors would use for acquiring used cars for their rental fleet. Since there is complexity in determining the prices of cars due to various factors like COE, OMV and Sales Upselling, our model will reduce the frustrations and time consumption of used car purchases. 
# 
# In this study, we would be utilizing data science processes from data collection (web-scraping: BeautifulSoup, Python), data cleaning, exploratory data analysis to the model training and testing stage. The source of data comes SgCarMart, an online car sales portal in Singapore. 

# In[3]:


import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, ElasticNet, ElasticNetCV

import  scipy.signal.signaltools

def _centered(arr, newsize):
    # Return the center newsize portion of the array.
    newsize = np.asarray(newsize)
    currsize = np.array(arr.shape)
    startind = (currsize - newsize) // 2
    endind = startind + newsize
    myslice = [slice(startind[k], endind[k]) for k in range(len(endind))]
    return arr[tuple(myslice)]

scipy.signal.signaltools._centered = _centered
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')


# In[4]:


df_main = pd.read_csv('sgcarmart_used_cars_prices7.csv',index_col=0)
df_main.sample(5)


# In[5]:


df_clean = df_main.drop(['LISTING_URL', 'SCRAPE_DATE'],axis=1)


# In[6]:


dropped_data=df_clean.dropna()


# In[7]:


df_clean=dropped_data
df_main['SCRAPE_DATE'] = pd.to_datetime(df_main['SCRAPE_DATE'])
df_clean['MANUFACTURED_YEAR'] = df_clean['MANUFACTURED_YEAR'].astype(int)
df_clean['CAR_AGE'] = df_main['SCRAPE_DATE'].dt.year  - df_clean['MANUFACTURED_YEAR'] # Obtaining values for age of car


# In[8]:


df_clean['POST_DATE'] = pd.to_datetime(df_clean['POST_DATE'])
df_clean['POST_AGE'] = (df_main['SCRAPE_DATE'] - df_clean['POST_DATE'])
df_clean['POST_AGE']=df_clean['POST_AGE'].dt.days


# In[9]:


# Transmission conversion -> 1 for auto, 0 for manual (just 1 column only)

df_clean['TRANSMISSION_CONVERT'] = df_clean['TRANSMISSION'].apply(lambda x: 1 if x == 'Auto' else 0)
df_clean.drop('TRANSMISSION',axis=1,inplace=True)
df_clean.rename(columns={'TRANSMISSION_CONVERT':"TRANSMISSION"}, inplace=True)  # Renaming column back


# In[10]:


veh_list=[]
for veh in df_clean['VEHICLE_TYPE'].unique():
    veh_list.append(veh)

veh_list.sort()
out = map(lambda x:x.lower(), veh_list)
veh_list = list(out) 


# In[11]:


df_clean['VEHICLE_TYPE']
df_encoded = pd.get_dummies(df_clean['VEHICLE_TYPE'], prefix='VEHICLE_TYPE')

# Concatenating the new columns to the original DataFrame
df_encoded = df_encoded.astype(int)
df_clean = pd.concat([df_clean, df_encoded], axis=1)


# ## Feature Engineering: Categorization of BRAND Column
# 

# In[12]:


# Renaming Brand Names to their actual names
df_clean2=df_clean
df_clean2.loc[df_clean2['BRAND'] == 'Aston','BRAND'] = 'Aston Martin'
df_clean2.loc[df_clean2['BRAND'] == 'Land','BRAND'] = 'Land Rover'
df_clean2.loc[df_clean2['BRAND'] == 'Alfa', 'BRAND'] = 'Alfa Romeo'
# Cleaning whitespaces from the values in "Brand" to prevent any messup later
df_clean2['BRAND'].apply(str.strip)


# In[13]:


category_brands = {
    'EXOTIC': ['Koenigsegg','Bugatti','Ferrari', 'Lamborghini','Aston Martin','McLaren','Hummer'],
    'ULTRA_LUXURY': ['Porsche','Maserati','Rolls-Royce', 'Land Rover','Bentley','Maybach'],
    'LUXURY': ['MINI','Mini','Alfa Romeo','Mercedes','Mercedes-Benz', 'BMW', 'Audi', 'Lexus','Jeep','Lotus','Volvo','Peugeot','Tesla','BYD','Acura','Cadillac','Jaguar','Infiniti','Chrysler','Lincoln','Genesis'],
    'MID_LEVEL': ['Volkswagen','Renault','Ford', 'Chevrolet'],
    'ECONOMY': ['Toyota','Honda','Hyundai', 'Kia', 'Nissan', 'Mazda','Mitsubishi','Subaru','Suzuki','Citroen','Proton','Ssangyong','Daihatsu','Fiat','Skoda','Opel','MG','SEAT','Perodua'],
    'OTHERS': []  # An empty list for unspecified brands
}

# Reversing the categorization based on the 'Brand' column
df_clean2['CAR_CATEGORY'] = df_clean2['BRAND'].apply(lambda x: next((category for category, brands in category_brands.items() if x in brands), 'OTHERS'))


# In[14]:


df_encoded = pd.get_dummies(df_clean2['CAR_CATEGORY'], prefix='CAR_CATEGORY')

# Concatenating the new columns to the original DataFrame
df_encoded = df_encoded.astype(int)
df_clean2 = pd.concat([df_clean2, df_encoded], axis=1)


# In[15]:


df_clean_log=df_clean2.copy()
df_clean_log["MILEAGE_KM"] = df_clean_log['MILEAGE_KM'].apply(np.log)

df_clean_log["DEPRE_VALUE_PER_YEAR"] = df_clean_log['DEPRE_VALUE_PER_YEAR'].apply(np.log)
df_clean_log["ROAD_TAX_PER_YEAR"] = df_clean_log['ROAD_TAX_PER_YEAR'].apply(np.log)
df_clean_log["DEREG_VALUE_FROM_SCRAPE_DATE"] = df_clean_log['DEREG_VALUE_FROM_SCRAPE_DATE'].apply(np.log)
df_clean_log["OMV"] = df_clean_log['OMV'].apply(np.log)
df_clean_log["ARF"] = df_clean_log['ARF'].apply(np.log)
df_clean_log["COE_FROM_SCRAPE_DATE"] = df_clean_log['COE_FROM_SCRAPE_DATE'].apply(np.log)
#df_clean_log["DAYS_OF_COE_LEFT"] = df_clean_log['DAYS_OF_COE_LEFT'].apply(np.log)
df_clean_log["ENGINE_CAPACITY_CC"] = df_clean_log['ENGINE_CAPACITY_CC'].apply(np.log)
df_clean_log["CURB_WEIGHT_KG"] = df_clean_log['CURB_WEIGHT_KG'].apply(np.log)


# In[16]:


#Drop 'ARF', 'ROAD_TAX_PER_YEAR','REG_DATE','MANUFACTURED_YEAR','VEHICLE_TYPE','POST_DATE','CAR_CATEGORY'
df_clean_log.drop('ARF', axis=1, inplace=True)
df_clean_log.drop('ROAD_TAX_PER_YEAR', axis=1, inplace=True)

#Dropping columns not needed in our regression as they have been encoded 
df_clean_log.drop('BRAND', axis=1, inplace=True)
df_clean_log.drop('REG_DATE', axis=1, inplace=True)
df_clean_log.drop('MANUFACTURED_YEAR', axis=1, inplace=True)
df_clean_log.drop('VEHICLE_TYPE', axis=1, inplace=True)
df_clean_log.drop('POST_DATE', axis=1, inplace=True)
df_clean_log.drop('CAR_CATEGORY', axis=1, inplace=True)


# In[17]:


df_clean_log.to_csv('clean_log_data.csv', index=False)


# In[ ]:




