from training.configuration_manager.configuration import ConfigurationManager
from training.components.common.feature_extraction import FeatureExtraction
from training.custom_logging import info_logger
import sys

PIPELINE = "Feature Extraction Training Pipeline"

class FeatureExtractionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        feature_extraction_config = config.get_feature_extraction_config()

        feature_extraction =  FeatureExtraction(config = feature_extraction_config)
        feature_extraction.extract_features()
            


if __name__ == "__main__":
    info_logger.info(f">>>>>>>> {PIPELINE} sttarted <<<<<<<<<")
    obj = FeatureExtractionPipeline()
    obj.main()
    info_logger.info(f">>>>>>>> {PIPELINE} completed <<<<<<<<<")