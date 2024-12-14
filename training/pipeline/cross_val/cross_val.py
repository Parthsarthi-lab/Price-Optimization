from training.configuration_manager.configuration import ConfigurationManager
from training.components.cross_val.cross_val import CrossVal
from training.custom_logging import info_logger
import sys
import gc

PIPELINE = "Cross Validation Training Pipeline"

class CrossValPipeline:

    def __init__(self):
        pass

    def main(self):
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


        


if __name__ == "__main__":

    info_logger.info(f">>>>> {PIPELINE} started <<<<")
    obj = CrossValPipeline()
    obj.main()
    info_logger.info(f">>>>>>>> {PIPELINE} completed <<<<<<<<<")