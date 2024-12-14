import os 
import os
from pathlib import Path
import logging
# This file creates the required files in the project directory.

logging.basicConfig(filename="templates.log", level=logging.INFO)


root_directory_files =[
    ".gitignore",
    "execute_cross_validation.py",
    "execute_final_model_training.py",
    "README.md",
    "requirements.txt",
    "setup.py",
    "common/__init__.py"
]

training_pipeline_files = [
    "training/custom_logging.py",
    "training/exception.py",
    "training/__init__.py",
    "training/components/__init__.py",
    "training/components/common/__init__.py",
    "training/components/common/data_ingestion.py",
    "training/components/common/data_validation.py",
    "training/components/common/feature_extraction.py",
    "training/components/cross_val/nested_cross_val.py",
    "training/components/cross_val/__init__.py",
    "training/components/final_train/model_training.py",
    "training/components/final_train/__init__.py",
    "training/components/final_train/model_evaluation.py",
    "training/components/final_train/feature_engineering.py",
    "training/config/config.yaml",
    "training/config/params.yaml",
    "training/config/schema.yaml",
    "training/configuration_manager/configuration.py",
    "training/configuration_manager/__init__.py",
    "training/constants/__init__.py",
    "training/entity/config_entity.py",
    "training/entity/__init__.py",
    "training/pipeline/__init__.py",
    "training/pipeline/common/__init__.py",
    "training/pipeline/common/data_ingestion.py",
    "training/pipeline/common/data_validation.py",
    "training/pipeline/common/feature_extraction.py",
    "training/pipeline/cross_val/nested_cross_val.py",
    "training/pipeline/cross_val/__init__.py",
    "training/pipeline/final_train/model_training.py",
    "training/pipeline/final_train/__init__.py",
    "training/pipeline/final_train/model_evaluation.py",
    "training/pipeline/final_train/feature_engineering.py",
    "training/utils/__init__.py",
    "training/utils/common.py"
    ]

deployment_pipeline_files =[
    "deployment/app.py",
    "deployment/custom_logging.py",
    "deployment/exception.py",
    "deployment/__init__.py",
    "deployment/components/image_processing.py",
    "deployment/components/feature_extraction.py",
    "deployment/components/prediction.py",
    "deployment/components/feature_engineering.py",
    "deployment/pipeline/__init__.py",
    "deployment/pipeline/prediction_pipeline.py",
    "deployment/static/styles.css",
    "deployment/templates/index.html",
    "deployment/templates/predict.html",
    "deployment/templates/upload_image.html",
    ""
]

for list_of_files in [root_directory_files,training_pipeline_files,deployment_pipeline_files]:
    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)

        if filedir !="":
            os.makedirs(filedir,exist_ok=True)
            logging.info(f"Creating directory; {filedir} for the file: {filename}")

        if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
            with open(filepath,"w") as f:
                pass
                logging.info(f"Creating empty file: {filepath}")

        else:
            logging.info(f"{filename} already exists")