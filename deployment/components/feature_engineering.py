from deployment.custom_logging import info_logger, error_logger
from deployment.exception import FeatureEngineeringError, handle_exception
import numpy as np
import sys
import os
from pathlib import Path
import joblib

class FeatureEngineering:
    def __init__(self):
        pass

    def transform_data(self, data):
        try:
            product_id_pipeline_path = "artifacts/feature_engineering/product_id.joblib"
            product_cat_name_pipeline_path = "artifacts/feature_engineering/product_cat_name.joblib"
            
            product_id_pipeline = joblib.load(product_id_pipeline_path)
            product_cat_name_pipeline = joblib.load(product_cat_name_pipeline_path)

            transformed_data = product_id_pipeline.transform(data)
            transformed_data = product_cat_name_pipeline.transform(transformed_data)

            return transformed_data
        except Exception as e:
            handle_exception(e, FeatureEngineeringError)


if __name__ == "__main__":

    data = np.array([[122,34.5,89]])
    feature_engineering = FeatureEngineering()
    transformed_data = feature_engineering.transform_data(data)
    print(transformed_data)