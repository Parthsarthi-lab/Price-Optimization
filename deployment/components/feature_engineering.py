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
            transformation_pipeline_path = "artifacts/feature_engineering/pipeline.joblib"
            transformation_pipeline = joblib.load(transformation_pipeline_path)

            transformed_data = transformation_pipeline.transform(data)

            return transformed_data
        except Exception as e:
            handle_exception(e, FeatureEngineeringError)


if __name__ == "__main__":

    data = np.array([[122,34.5,89]])
    feature_engineering = FeatureEngineering()
    transformed_data = feature_engineering.transform_data(data)
    print(transformed_data)