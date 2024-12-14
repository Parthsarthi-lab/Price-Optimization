from dataclasses import dataclass
from pathlib import Path 

#1
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source: Path
    data_dir: Path
    STATUS_FILE: str

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_dir: Path
    all_schema: dict
    STATUS_FILE: str

@dataclass(frozen=True)
class FeatureExtractionConfig:
    root_dir: Path
    data_dir: Path
    STATUS_FILE: str

@dataclass(frozen=True)
class CrossValConfig:
    root_dir: Path
    data_dir: Path
    final_train_data_path: Path
    final_test_data_path: Path
    best_model_params: Path
    STATUS_FILE: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    final_train_data_path: Path
    final_test_data_path: Path
    best_model_params: Path
    STATUS_FILE: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    final_test_data_path: Path
    model_path: Path
    STATUS_FILE: str