#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# Our project aims to identify an optimal pricing model using regression techniques to quantify what the reasonable price range of a car would be, which Atlas Motors would use for acquiring used cars for their rental fleet. Since there is complexity in determining the prices of cars due to various factors like COE, OMV and Sales Upselling, our model will reduce the frustrations and time consumption of used car purchases. 
# 
# In this study, we would be utilizing data science processes from data collection (web-scraping: BeautifulSoup, Python), data cleaning, exploratory data analysis to the model training and testing stage. The source of data comes SgCarMart, an online car sales portal in Singapore. 

# In[5]:


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


# In[6]:


df_clean_log = pd.read_csv('clean_log_data.csv')


# In[14]:


df_clean_log


# In[7]:


x_var=df_clean_log.drop('PRICE', axis=1)


y= df_clean_log['PRICE']

test_size = 0.20
seed = 7
X_train, X_test, y_train, y_test = train_test_split(x_var, y, test_size=test_size, random_state=seed)


# In[8]:


num_folds = 10
seed = 7
scoring = 'neg_mean_squared_error'


# In[9]:


import warnings
warnings.filterwarnings("ignore")
scaler = StandardScaler().fit(X_train)
rescaledX = scaler.transform(X_train)
model = ExtraTreesRegressor(n_estimators=400)
model.fit(rescaledX, y_train)
# transform the validation dataset
rescaledValidationX = scaler.transform(X_test)
predictions = model.predict(rescaledValidationX)
print("MSE : {}".format(round(mean_squared_error(y_test, predictions), 3)))
print("RMSE : {}".format(round(np.sqrt(mean_squared_error(y_test, predictions)), 3)))
print("R squared error : {}".format(round(r2_score(y_test,predictions), 3)))


# In[ ]:




