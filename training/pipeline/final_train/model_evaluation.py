from training.configuration_manager.configuration import ConfigurationManager
from training.components.final_train.model_evaluation import ModelEvaluation
from training.custom_logging import info_logger
import sys

PIPELINE = "Final Model Evaluation Pipeline"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()

        model_evluation = ModelEvaluation(config = model_evaluation_config)
        final_model = model_evluation.load_model()
        xtest, ytest = model_evluation.load_test_data()

        model_evluation.evaluate_model(final_model, xtest, ytest)
            


if __name__ == "__main__":  
    info_logger.info(f">>>>> {PIPELINE} started <<<<")
    obj = ModelEvaluationTrainingPipeline()
    obj.main()
    info_logger.info(f">>>>>>>> {PIPELINE} completed <<<<<<<<<")