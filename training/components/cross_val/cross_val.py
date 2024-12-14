import os
import sys
import json
import joblib
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.metrics import mean_squared_error

from sklearn.preprocessing import LabelEncoder

from training.custom_logging import info_logger, error_logger
from training.exception import CrossValError, handle_exception

from training.configuration_manager.configuration import ConfigurationManager
from training.entity.config_entity import CrossValConfig

class CrossVal:
    def __init__(self, config: CrossValConfig):
        self.config = config


    @staticmethod
    def is_json_serializable(value):
      """
      Check if a value is JSON serializable.
      """
      try:
          json.dumps(value)
          return True
      except (TypeError, OverflowError):
          return False
      

    def split_data_for_final_train(self, X, y):
        try:
            info_logger.info("Data split for final train started")
            
            xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
            
            info_logger.info("Data split for final train completed")
            return xtrain, xtest, ytrain, ytest
        except Exception as e:
            handle_exception(e, CrossValError)
    
    def save_data_for_final_train(self, xtrain, xtest, ytrain, ytest):
        try:
            info_logger.info("Saving data for final train started")

            final_train_data_path = self.config.final_train_data_path
            final_test_data_path = self.config.final_test_data_path

            # Save xtrain and ytrain  to Train.npz
            # Save xtest and ytest to Test.npz
            np.savez(os.path.join(final_train_data_path, 'Train.npz'), xtrain=xtrain, ytrain=ytrain)
            np.savez(os.path.join(final_test_data_path, 'Test.npz'),  xtest=xtest, ytest=ytest)

            info_logger.info("Saved data for final train")
        except Exception as e:
            handle_exception(e, CrossValError)
    

    def feature_engineering(self):
        try:
            info_logger.info("Feature Engineering for Cross Val Component started")
            
            df = pd.read_csv(self.config.data_dir)
            
            # Convert to datetime
            df['month_year'] = pd.to_datetime(df['month_year'], format='%d-%m-%Y')

            # Extract numeric features from datetime
            df['year'] = df['month_year'].dt.year
            df['month'] = df['month_year'].dt.month

            df.drop(['month_year'], axis=1, inplace=True)

            # Lable Encoding for categorical data
            product_id_mapping = LabelEncoder()
            product_cat_name_mapping = LabelEncoder()

            df['product_id'] = product_id_mapping.fit_transform(df['product_id'])
            df['product_category_name'] = product_cat_name_mapping.fit_transform(df['product_category_name'])


            # Save label encoder to artifacts folder
            product_id_path = os.path.join(self.config.root_dir,"product_id.joblib")
            product_cat_name_path = os.path.join(self.config.root_dir,"product_cat_name.joblib")
            joblib.dump(product_id_mapping, product_id_path)
            joblib.dump(product_cat_name_mapping, product_cat_name_path)

            info_logger.info("Feature Engineering for Cross Val Component completed")

            return df
        except Exception as e:
            handle_exception(e, CrossValError)

    def run_cross_val(self, X, y):
        try:
            info_logger.info("Cross Validation Started")

            # Initialize the Random Forest Regressor
            rf_regressor = RandomForestRegressor(random_state=42)
            k = 10
            kf = KFold(n_splits=k, shuffle=True, random_state=42)

            # Variables to track the best model and its RMSE
            best_hyperparameters = None
            lowest_rmse = float('inf')  # Start with an infinitely high RMSE value
            best_model = None

            # Perform K-Fold Cross-Validation
            mse_scores = []

            for train_index, test_index in kf.split(X):
                # Split the data into training and testing sets
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]

                # Ensure y is 1D
                y_train = y_train.values.ravel()
                y_test = y_test.values.ravel()

                # Train the Random Forest Regressor
                rf_regressor.fit(X_train, y_train)

                # Make predictions on the test set
                y_pred = rf_regressor.predict(X_test)

                # Calculate the Mean Squared Error (MSE)
                mse = mean_squared_error(y_test, y_pred)
                mse_scores.append(mse)
                rmse = np.sqrt(mse)

                # Check if this model is the best so far
                if rmse < lowest_rmse:
                    lowest_rmse = rmse
                    best_hyperparameters = rf_regressor.get_params()  # Get current model's hyperparameters
                    best_model = rf_regressor

            # Final results
            rmse_scores = np.sqrt(mse_scores)

            # Store the best model's information
            best_scores = lowest_rmse
            best_params = best_hyperparameters


            with open(self.config.STATUS_FILE, "a") as f:
                f.write(f"Best params for Model: {str(best_params)}\n")
                f.write(f"Best scoring(RMSE) for Model: {str(best_scores)}\n")

            best_model_params_path = os.path.join(self.config.best_model_params, f'best_params.json')
            best_model_params = best_model.get_params()
            serializable_params = {k: v for k, v in best_model_params.items() if self.is_json_serializable(v)}
            
            with open(best_model_params_path, 'w') as f:
                json.dump(serializable_params, f, indent=4)


            info_logger.info("Cross Validation completed")
        except Exception as e:
            handle_exception(e, CrossValError)

if __name__ == "__main__":
    config = ConfigurationManager()
    cross_val_config = config.get_cross_val_config()

    cross_val = CrossVal(config=cross_val_config)

    # Feature Engineering
    df = cross_val.feature_engineering()

    X = df.drop("qty", axis=1)
    y = df["qty"]
    

    # Split the data into train and test sets for final train
    xtrain, xtest, ytrain, ytest = cross_val.split_data_for_final_train(X,y)

    # Save xtrain, xtest, ytain, ytest to be used final train
    cross_val.save_data_for_final_train(xtrain, xtest, ytrain, ytest)

    # Run cross validation
    cross_val.run_cross_val(xtrain, ytrain)