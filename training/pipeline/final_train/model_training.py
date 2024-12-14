from training.configuration_manager.configuration import ConfigurationManager
from training.components.final_train.model_training import ModelTrainer
from training.custom_logging import info_logger
import sys

PIPELINE = "Final Model Training Pipeline"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()

        model_trainer = ModelTrainer(config = model_trainer_config)
        xtrain, xtest, ytrain, ytest = model_trainer.load_transformed_data()
        model = model_trainer.train_model(xtrain, xtest, ytrain, ytest)
        model_trainer.save_model(model)
        
if __name__ == "__main__":

        info_logger.info(f">>>>> {PIPELINE} started <<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        info_logger.info(f">>>>>>>> {PIPELINE} completed <<<<<<<<<")