import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load data (assuming the CSV file is in the same directory as this script)
csv__file__path = 'clean_log_data.csv'

# Load data
df_clean_log = pd.read_csv(csv__file__path)

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
