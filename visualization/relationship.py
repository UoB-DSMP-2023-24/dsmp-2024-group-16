import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the data
data_path = 'Tape.csv'
data = pd.read_csv(data_path)

# Prepare the data
X = data[['Volume']]  # Predictor variable
y = data['Close']  # Response variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
lr_model = LinearRegression()
dt_model = DecisionTreeRegressor(random_state=42)
knn_model = KNeighborsRegressor(n_neighbors=5)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the models
lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)
knn_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_lr = lr_model.predict(X_test)
y_pred_dt = dt_model.predict(X_test)
y_pred_knn = knn_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

# Calculate the performance metrics
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)

mse_knn = mean_squared_error(y_test, y_pred_knn)
r2_knn = r2_score(y_test, y_pred_knn)

mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# RMSE calculations
rmse_lr = np.sqrt(mse_lr)
rmse_dt = np.sqrt(mse_dt)
rmse_knn = np.sqrt(mse_knn)
rmse_rf = np.sqrt(mse_rf)

# Model names and their R-squared and RMSE values
models = ['Linear Regression', 'Decision Tree', 'KNN', 'Random Forest']
r2_values = [r2_lr, r2_dt, r2_knn, r2_rf]
rmse_values = [rmse_lr, rmse_dt, rmse_knn, rmse_rf]

# Plotting R-squared values
plt.figure(figsize=(10, 6))
plt.bar(models, r2_values, color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Model')
plt.ylabel('R-squared Value')
plt.title('Comparison of Regression Models Based on R-squared Value')
plt.ylim(0, 1)
plt.grid(axis='y')
plt.show()

# Plotting RMSE values
plt.figure(figsize=(10, 6))
plt.bar(models, rmse_values, color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Model')
plt.ylabel('RMSE Value')
plt.title('Comparison of Regression Models Based on RMSE Value')
plt.grid(axis='y')
plt.show()
