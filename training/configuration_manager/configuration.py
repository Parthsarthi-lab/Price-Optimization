from training.constants import *
from training.utils.common import read_yaml, create_directories
from training.entity.config_entity import DataIngestionConfig
from training.entity.config_entity import DataValidationConfig
from training.entity.config_entity import FeatureExtractionConfig
from training.entity.config_entity import CrossValConfig
from training.entity.config_entity import ModelTrainerConfig
from training.entity.config_entity import ModelEvaluationConfig

class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH,
            schema_filepath = SCHEMA_FILE_PATH) :
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])
#1
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source=config.source,
            data_dir=config.data_dir,
            STATUS_FILE=config.STATUS_FILE
        )
        return data_ingestion_config
    
#2
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            all_schema=schema,
            STATUS_FILE=config.STATUS_FILE
        )
        return data_validation_config
    
#3
    def get_feature_extraction_config(self) -> FeatureExtractionConfig:
        config = self.config.feature_extraction

        create_directories([config.root_dir])
        
        feature_extraction_config = FeatureExtractionConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            STATUS_FILE=config.STATUS_FILE
        )
        return feature_extraction_config
    
    #4
    def get_cross_val_config(self) -> CrossValConfig:
            config = self.config.cross_val
            create_directories([config.root_dir])
            create_directories([config.final_train_data_path, config.final_test_data_path])
            create_directories([ config.best_model_params])

            cross_val_config = CrossValConfig(
                root_dir = config.root_dir,
                data_dir= config.data_dir,
                final_train_data_path = config.final_train_data_path,
                final_test_data_path= config.final_test_data_path,
                best_model_params= config.best_model_params,
                STATUS_FILE= config.STATUS_FILE
            )

            return cross_val_config

    def get_model_trainer_config(self) -> ModelTrainerConfig :        
            config = self.config.model_trainer

            create_directories([config.root_dir])

            model_trainer_config = ModelTrainerConfig(
                root_dir = config.root_dir,
                final_train_data_path=config.final_train_data_path,
                final_test_data_path=config.final_test_data_path,
                best_model_params=config.best_model_params,
                STATUS_FILE= config.STATUS_FILE
            )

            return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:

        config = self.config.model_evaluation
        
        create_directories([config.root_dir])
        

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            final_test_data_path=config.final_test_data_path,
            model_path=config.model_path,
            STATUS_FILE = config.STATUS_FILE
        )

        return model_evaluation_config