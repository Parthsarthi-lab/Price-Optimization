from deployment.custom_logging import info_logger, error_logger
from deployment.exception import PredictionError, handle_exception

from deployment.components.feature_engineering import FeatureEngineering
from deployment.components.optimize_price import OptimizePrice

import numpy as np
import os
import sys
from pathlib import Path

class OptimizationPipeline:
    def __init__(self):
        pass

    def predict(self, input):
        feature_engineering = FeatureEngineering()
        transformed_data = feature_engineering.transform_data(input)

        prediction = OptimizePrice()
        predicted_price = prediction.optimize_price(transformed_data)

        return predicted_price


if __name__ == "__main__":
    opt_pipeline = OptimizationPipeline()
    input = np.array([["bed1","bed_bath_table",3,4,5,6,7,8,9,10,11,12,13,14,15,16]])
    optimized_price = opt_pipeline.predict(input)
    print(optimized_price)