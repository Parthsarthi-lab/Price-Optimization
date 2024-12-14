from deployment.custom_logging import info_logger, error_logger
from deployment.exception import PredictionError, handle_exception
import numpy as np
import joblib
import os
import sys
from pathlib import Path

class Prediction:
    def __init__(self):
        pass

    def predict(self, data):
        try:
            model_path = "artifacts/model_trainer/final_model.joblib"
            model = joblib.load(model_path)

            predicted_qty = model.predict(data)

            return predicted_qty[0]
        except Exception as e:
            handle_exception(e, PredictionError)

if __name__ == "__main__":
    prediction = Prediction()
    data = np.array([[ 0 , 0 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ,10, 11, 12, 13, 14, 15, 16]])
    predicted_qt = prediction.predict(data)
    print(predicted_qt)