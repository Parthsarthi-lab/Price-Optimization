import os
import sys
import joblib
from pathlib import Path

import numpy as np

from deployment.custom_logging import info_logger, error_logger
from deployment.exception import BayesianOptimizationError, handle_exception

from skopt import gp_minimize
from skopt.space import Real

class OptimizePrice:
    def __init__(self):
        pass

    def predict(self, data):
        try:
            model_path = "artifacts/model_trainer/final_model.joblib"
            model = joblib.load(model_path)

            predicted_qty = model.predict(data)

            return predicted_qty[0]
        except Exception as e:
            handle_exception(e, BayesianOptimizationError)
    

    def optimize_price(self,*features):

        try:
            features = np.array([val for val in features]).reshape(1,-1)
            predicted_qty = self.predict(features)
            
            def objective_function(price):
                
                # Calculate profit: (Price - Cost) * Predicted Quantity
                avg_freight_price= 20.68226996
                cost = avg_freight_price # Replace with your actual average cost
                profit = (price[0] - cost) * predicted_qty
                profit = -(profit)
                
                return profit

            # Define search space for unit_price
            search_space = [Real(10, 400, name="unit_price")]

            # Run Bayesian Optimization
            result = gp_minimize(
                func=objective_function,            # Profit function
                dimensions=search_space,
                acq_func="EI",          # Expected Improvement
                n_calls=10,             # Number of iterations
                random_state=42
            )
            
            optimal_price = result.x[0]
            return optimal_price
        
        except Exception as e:
            handle_exception(e, BayesianOptimizationError)

if __name__ == "__main__":
    price_optimizer = OptimizePrice()
    features = np.array([[ 0 , 0 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ,10, 11, 12, 13, 14, 15, 16]])

    optimal_price = price_optimizer.optimize_price(features)
    print(f"Optimal Price: {optimal_price}")