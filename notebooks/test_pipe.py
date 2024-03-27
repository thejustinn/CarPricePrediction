import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, ElasticNet, ElasticNetCV


class DataPipeLine :

    def __init__(self, data_source):
        self.data_path = data_source
        self.data = None
        self.scaled_data = None
        self.regressor.data = None
        self.number = 0.4

    def load_data(self):
        self.data = pd.read_csv(self.data_path)
        return(self.number)

    def clean_data(self):
        data_clean = self.data.drop(['LISTING_URL', 'SCRAPE_DATE'],axis=1)
        data_clean.dropna()
        data_clean['SCRAPE_DATE'] = pd.to_datetime(self.data['SCRAPE_DATE'])
        df_clean['MANUFACTURED_YEAR'] = df_clean['MANUFACTURED_YEAR'].astype(int)


        df_clean=dropped_data
        df_main['SCRAPE_DATE'] = pd.to_datetime(df_main['SCRAPE_DATE'])
        df_clean['MANUFACTURED_YEAR'] = df_clean['MANUFACTURED_YEAR'].astype(int)
        df_clean['CAR_AGE'] = df_main['SCRAPE_DATE'].dt.year  - df_clean['MANUFACTURED_YEAR'] # Obtaining values for age of car


    def scale_data(self):
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.data)

    def regression(self):
        regressor = ExtraTreesRegressor(n_estimators=400)
        self.regressor = regressor.fit(self.data)

    def run_pipeline(self, n_components):
        self.load_data()
        self.scale_data()
        self.perform_pca(n_components)

