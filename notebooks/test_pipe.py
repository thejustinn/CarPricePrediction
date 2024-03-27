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
<<<<<<< Updated upstream
        self.regressor_data = None
=======
>>>>>>> Stashed changes

    def load_data(self):
        self.data = pd.read_csv(self.data_path)

    def clean_data(self):
<<<<<<< Updated upstream
        data_clean = self.data.drop(['LISTING_URL', 'SCRAPE_DATE'],axis=1)
        data_clean.dropna()
        data_clean['SCRAPE_DATE'] = pd.to_datetime(self.data['SCRAPE_DATE'])
        df_clean['MANUFACTURED_YEAR'] = df_clean['MANUFACTURED_YEAR'].astype(int)

=======
        df_clean = self.data.drop(['LISTING_URL', 'SCRAPE_DATE'],axis=1)
        dropped_data=df_clean.dropna()
>>>>>>> Stashed changes
        df_clean=dropped_data
        
        self.data['SCRAPE_DATE'] = pd.to_datetime(self.data['SCRAPE_DATE'])
        df_clean['MANUFACTURED_YEAR'] = df_clean['MANUFACTURED_YEAR'].astype(int)
        df_clean['CAR_AGE'] = self.data['SCRAPE_DATE'].dt.year  - df_clean['MANUFACTURED_YEAR']
        
        df_clean['POST_DATE'] = pd.to_datetime(df_clean['POST_DATE'])
        df_clean['POST_AGE'] = (self.data['SCRAPE_DATE'] - df_clean['POST_DATE'])
        df_clean['POST_AGE']=df_clean['POST_AGE'].dt.days

<<<<<<< Updated upstream
=======
        df_clean['TRANSMISSION_CONVERT'] = df_clean['TRANSMISSION'].apply(lambda x: 1 if x == 'Auto' else 0)
        df_clean.drop('TRANSMISSION',axis=1,inplace=True)
        df_clean.rename(columns={'TRANSMISSION_CONVERT':"TRANSMISSION"}, inplace=True) 

        veh_list=[]
        for veh in df_clean['VEHICLE_TYPE'].unique():
            veh_list.append(veh)

        veh_list.sort()
        out = map(lambda x:x.lower(), veh_list)
        veh_list = list(out) 

        df_clean['VEHICLE_TYPE']
        df_encoded = pd.get_dummies(df_clean['VEHICLE_TYPE'], prefix='VEHICLE_TYPE')

        # Concatenating the new columns to the original DataFrame
        df_encoded = df_encoded.astype(int)
        df_clean = pd.concat([df_clean, df_encoded], axis=1)

        df_clean2=df_clean
        df_clean2.loc[df_clean2['BRAND'] == 'Aston','BRAND'] = 'Aston Martin'
        df_clean2.loc[df_clean2['BRAND'] == 'Land','BRAND'] = 'Land Rover'
        df_clean2.loc[df_clean2['BRAND'] == 'Alfa', 'BRAND'] = 'Alfa Romeo'
        # Cleaning whitespaces from the values in "Brand" to prevent any messup later
        df_clean2['BRAND'].apply(str.strip)

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

        df_encoded = pd.get_dummies(df_clean2['CAR_CATEGORY'], prefix='CAR_CATEGORY')

        # Concatenating the new columns to the original DataFrame
        df_encoded = df_encoded.astype(int)
        df_clean2 = pd.concat([df_clean2, df_encoded], axis=1)

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

        df_clean_log.drop('ARF', axis=1, inplace=True)
        df_clean_log.drop('ROAD_TAX_PER_YEAR', axis=1, inplace=True)

        #Dropping columns not needed in our regression as they have been encoded 
        df_clean_log.drop('BRAND', axis=1, inplace=True)
        df_clean_log.drop('REG_DATE', axis=1, inplace=True)
        df_clean_log.drop('MANUFACTURED_YEAR', axis=1, inplace=True)
        df_clean_log.drop('VEHICLE_TYPE', axis=1, inplace=True)
        df_clean_log.drop('POST_DATE', axis=1, inplace=True)
        df_clean_log.drop('CAR_CATEGORY', axis=1, inplace=True)
        df_clean_log.drop(columns=df_clean_log.columns[0], axis=1,  inplace=True)
        return df_clean_log
        


>>>>>>> Stashed changes
    def scale_data(self):
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.data)

    def regression(self):
        regressor = ExtraTreesRegressor(n_estimators=400)
        self.regressor = regressor.fit(self.data)

    def run_pipeline(self, n_components):
        self.load_data()
        self.clean_data()
        self.scale_data()
<<<<<<< Updated upstream
        self.regression()
        self.perform_pca(n_components)
=======
       
>>>>>>> Stashed changes

