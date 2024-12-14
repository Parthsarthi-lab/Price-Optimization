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