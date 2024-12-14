import os
import sys
import pandas as pd
import numpy as np

from training.exception import FeautreExtractionError, handle_exception
from training.custom_logging import info_logger, error_logger

from training.entity.config_entity import FeatureExtractionConfig
from training.configuration_manager.configuration import ConfigurationManager


class FeatureExtraction:
    def __init__(self, config: FeatureExtractionConfig):
        self.config = config

    def extract_features(self):
        try:
            info_logger.info("Feature Extraction component started")

            status = False
            df = pd.read_csv(self.config.data_dir)
            # we are also removing total_price as it will leak information about qty(our target variable)
            useful_col = ['product_id', 'product_category_name', 'month_year', 'qty',
                'freight_price', 'unit_price', 'comp_1', 'ps1', 'fp1', 
                'comp_2', 'ps2', 'fp2', 'comp_3', 'ps3', 'fp3', 'lag_price']
            df = df[useful_col].copy(deep=True)
            
            save_path = os.path.join(self.config.root_dir, "features_extracted.csv")
            df.to_csv(save_path, index=False)

            status = True
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Feature Extraction status: {status}")

            info_logger.info("Feature Extraction Component completed")
        except Exception as e:
            status = False
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Feature Extraction status: {status}")
            handle_exception(e, FeautreExtractionError)

if __name__ == "__main__":
    config = ConfigurationManager()
    feature_extraction_config = config.get_feature_extraction_config()

    feature_extraction =  FeatureExtraction(config = feature_extraction_config)
    feature_extraction.extract_features()