import os 
import sys
from pathlib import Path
import shutil

from training.exception import DataIngestionError, handle_exception
from training.custom_logging import info_logger, error_logger

from training.entity.config_entity import DataIngestionConfig
from training.configuration_manager.configuration import ConfigurationManager


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            status = "Fail"
            self.config = config
            status = "Success"
        except Exception as e:
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Data Ingestion status: {status}")
            handle_exception(e, DataIngestionError)
            

    def save_data(self):
        try:
            info_logger.info("Data Ingestion Component started")
            status = False
            data_file_path = os.path.join(self.config.data_dir, "retail_price.csv")

            if not os.path.exists(data_file_path):
                shutil.copy(self.config.source, self.config.data_dir)
                status = True

                with open(self.config.STATUS_FILE, "w") as f:
                    f.write(f"Data Ingestion status: {status}")

            info_logger.info(f"Data Ingestion Component completed")
        except Exception as e:
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Data Ingestion status: {status}")

            handle_exception(e, DataIngestionError)





if __name__ == "__main__":
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()

    data_ingestion = DataIngestion(config = data_ingestion_config)
    data_ingestion.save_data()