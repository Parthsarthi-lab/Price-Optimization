import sys
import os
import json
import joblib
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor

from training.exception import ModelTrainingError, handle_exception
from training.custom_logging import info_logger, error_logger

from training.entity.config_entity import ModelTrainerConfig
from training.configuration_manager.configuration import ConfigurationManager

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    @staticmethod
    def filter_hyperparams(params):
        # Extract only the parameters related to the classifier (RandomForestClassifier)
        hyperparams = {key.replace('regressor__', ''): value for key, value in params.items() if key.startswith('classifier__')}
        return hyperparams

    def load_transformed_data(self):
        try:
            info_logger.info("Loading Final Training Transformed Data")

            final_train_data_path = os.path.join(self.config.final_train_data_path, 'Train.npz')
            final_test_data_path = os.path.join(self.config.final_test_data_path,"Test.npz")

            final_train_data = np.load(final_train_data_path, allow_pickle=True)
            final_test_data = np.load(final_test_data_path, allow_pickle=True)

            xtrain = final_train_data["xtrain"]
            xtest = final_test_data["xtest"]
            ytrain = final_train_data["ytrain"]
            ytest = final_test_data["ytest"]


            info_logger.info("Loaded Final Training Transformed Data")

            return xtrain, xtest, ytrain, ytest
        except Exception as e:
            handle_exception(e, ModelTrainingError)

    def train_model(self, xtrain, xtest, ytrain, ytest):
        try:
            info_logger.info("Training final model started")

            # Construct the full path to the hyperparameters file
            hyperparams_file_path = os.path.join(self.config.best_model_params, "best_params.json")
            
            # Load the hyperparameters from the JSON file
            with open(hyperparams_file_path, 'r') as f:
                hyperparams = json.load(f)

            # Filter the hyperparameters of the linear regression model
            hyperparams = self.filter_hyperparams(hyperparams)

            final_model = RandomForestRegressor(**hyperparams)

            final_model.fit(xtrain, ytrain)

            info_logger.info("Final model trained")

            return final_model
        except Exception as e:
            handle_exception(e, ModelTrainingError)

    def save_model(self, model):
        try:
            info_logger.info("Saving final model started")

            model_path = os.path.join(self.config.root_dir, "final_model.joblib")
            joblib.dump(model, model_path)


            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Model Training status: True")

            info_logger.info("Final model saved")
        except Exception as e:
            handle_exception(e, ModelTrainingError)

if __name__ == "__main__":
    config = ConfigurationManager()
    model_trainer_config = config.get_model_trainer_config()

    model_trainer = ModelTrainer(config = model_trainer_config)
    xtrain, xtest, ytrain, ytest = model_trainer.load_transformed_data()
    model = model_trainer.train_model(xtrain, xtest, ytrain, ytest)
    model_trainer.save_model(model)