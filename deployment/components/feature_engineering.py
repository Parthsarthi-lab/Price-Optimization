from deployment.custom_logging import info_logger, error_logger
from deployment.exception import FeatureEngineeringError, handle_exception
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
import joblib

class FeatureEngineering:
    def __init__(self):
        pass

    def transform_data(self, data):
        try:
            product_id_pipeline_path = "artifacts/cross_val/product_id.joblib"
            product_cat_name_pipeline_path = "artifacts/cross_val/product_cat_name.joblib"
            
            product_id_pipeline = joblib.load(product_id_pipeline_path)
            product_cat_name_pipeline = joblib.load(product_cat_name_pipeline_path)

            product_id_transformed = product_id_pipeline.transform([data[0][0]])
            product_cat_name_transformed = product_cat_name_pipeline.transform([data[0][1]])

            data[0][0] = product_id_transformed[0]
            data[0][1] = product_cat_name_transformed[0]

            data = data.astype(np.float64)
            transformed_data = data
            
            return transformed_data
        except Exception as e:
            handle_exception(e, FeatureEngineeringError)


if __name__ == "__main__":

    data = np.array([["bed1","bed_bath_table",3,4,5,6,7,8,9,10,11,12,13,14,15,16]])
    
    feature_engineering = FeatureEngineering()
    transformed_data = feature_engineering.transform_data(data)
    