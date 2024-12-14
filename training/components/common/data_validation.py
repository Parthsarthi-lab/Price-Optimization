import os
import sys
import pandas as pd
import numpy as np

from training.exception import DataValidationError, handle_exception
from training.custom_logging import info_logger, error_logger

from training.entity.config_entity import DataValidationConfig
from training.configuration_manager.configuration import ConfigurationManager


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self):
        """
        Validate the column names and dtypes of ingested data
        """
        try:
            info_logger.info("Data Validation Component started")

            status = False
            data_path = self.config.data_dir

            df = pd.read_csv(data_path)
            

            col_dtypes = df.dtypes
            info_logger.info(f"\n {col_dtypes}")
            schema = self.config.all_schema

            for i,j in zip(col_dtypes.index, schema.keys()):
                if i==j:
                    if col_dtypes[i]==schema[j]:
                        status = True
                        with open(self.config.STATUS_FILE, "w") as f:
                            f.write(f"Data Validation status: {status}")
                    else:
                        status = False
                        with open(self.config.STATUS_FILE, "w") as f:
                            f.write(f"Data Validation status: {status}")
                else:
                    status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Data Validation status: {status}")
            
            info_logger.info("Data Validation Component completed")
                
        except Exception as e:
            status = False
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Data Validation status: {status}")
            handle_exception(e, DataValidationError)


if __name__ == "__main__":
    config = ConfigurationManager()
    data_validation_config = config.get_data_validation_config()

    data_validation =  DataValidation(config = data_validation_config)
    data_validation.validate_data()