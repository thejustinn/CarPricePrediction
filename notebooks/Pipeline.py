import pandas as pd
import numpy as np
import scipy.signal.signaltools
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Data Preprocessing Steps
def preprocess_data(df):
    # Log transform certain columns
    df["MILEAGE_KM"] = df['MILEAGE_KM'].apply(np.log)
    df["DEPRE_VALUE_PER_YEAR"] = df['DEPRE_VALUE_PER_YEAR'].apply(np.log)
    df["ROAD_TAX_PER_YEAR"] = df['ROAD_TAX_PER_YEAR'].apply(np.log)
    df["DEREG_VALUE_FROM_SCRAPE_DATE"] = df['DEREG_VALUE_FROM_SCRAPE_DATE'].apply(np.log)
    df["OMV"] = df['OMV'].apply(np.log)
    df["COE_FROM_SCRAPE_DATE"] = df['COE_FROM_SCRAPE_DATE'].apply(np.log)
    df["ENGINE_CAPACITY_CC"] = df['ENGINE_CAPACITY_CC'].apply(np.log)
    df["CURB_WEIGHT_KG"] = df['CURB_WEIGHT_KG'].apply(np.log)

    # Drop unnecessary columns
    df.drop(['ARF', 'ROAD_TAX_PER_YEAR', 'REG_DATE', 'MANUFACTURED_YEAR', 'VEHICLE_TYPE', 'POST_DATE', 'CAR_CATEGORY', 'BRAND'], axis=1, inplace=True)
    
    return df

# Load data
df_clean_log = pd.read_csv('clean_log_data.csv')

# Preprocess data
df_clean_log = preprocess_data(df_clean_log)

# Split features and target
X = df_clean_log.drop('PRICE', axis=1)
y = df_clean_log['PRICE']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define pipeline steps
steps = [
    ('scaler', StandardScaler()),  # Standardize features
    ('regressor', RandomForestRegressor())  # RandomForestRegressor as the model
]

# Create pipeline
pipeline = Pipeline(steps)

# Train the model
pipeline.fit(X_train, y_train)

# Predictions on the test set
y_pred = pipeline.predict(X_test)

# Model evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R-squared Score:", r2)