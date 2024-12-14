from training.configuration_manager.configuration import ConfigurationManager
from training.components.common.data_validation import DataValidation
from training.custom_logging import info_logger
import sys

PIPELINE = "Data Validation Training Pipeline"

class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        # Load the data validation configuration object
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()

        # Passing the data validation configuration obj to the component
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_data()
            


if __name__ == "__main__":
    info_logger.info(f">>>>>>>> {PIPELINE} sttarted <<<<<<<<<")
    obj = DataValidationPipeline()
    obj.main()
    info_logger.info(f">>>>>>>> {PIPELINE} completed <<<<<<<<<")