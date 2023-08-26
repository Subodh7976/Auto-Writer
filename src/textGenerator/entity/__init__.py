from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path 
    source_url: str 
    local_data_file: Path 
    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path 
    status_file: Path 
    required_file: Path 
    
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path 
    local_data_path: Path 
    save_data_path: Path 
    tokenizer_name: str 
    block_size: int
    
@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path 
    data_path: Path 
    model_name: str 
    output_dir: Path 
    output_hidden_states: bool 
    overwrite_output_dir: bool 
    evaluation_strategy: str 
    save_strategy: str 
    compute_metrics: None 
    preprocess_logits_for_metrics: None 
    resume_from_checkpoint: None 
    
@dataclass(frozen=True)
class PredictionConfig:
    model_path: Path
    model_name: str
    