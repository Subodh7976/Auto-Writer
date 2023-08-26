from textSummarizer.constants import *
from utils.common import read_yaml, create_directories
from textSummarizer.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    PredictionConfig
)
from pathlib import Path


class ConfigurationManager:
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):
        '''
        creates a configuration manager class which manages configuration
        for various stages of development
        
        params:
            config_filepath: str = configuration yaml file path
            params_filepath: str = parameters yaml file path
        '''
        self.config = read_yaml(config_filepath)
        self.config = self.config.text_summarizer
        self.params = read_yaml(params_filepath)
        self.params = self.params.text_summarizer
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        '''
        creates and returns data ingestion configuration 
        
        returns:
            DataIngestionConfig: the configuration for data ingestion
        '''
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir, 
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )
        
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        '''
        creates and returns data validation configuration
        
        returns:
            DataValidationConfig: the configuration for data validation
        '''
        config = self.config.data_validation
        
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
            data_path=config.data_path
        )
        
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        '''
        creates and returns data transformation configuration
        
        returns:
            DataTransformationConfig: the configuration for data transformation
        '''
        config = self.config.data_transformation
        
        create_directories([config.root_dir])
        
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            train_dataset=config.train_dataset,
            val_dataset=config.val_dataset,
            tokenizer_name=config.tokenizer_name 
        )
        
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        '''
        creates and returns model trainer configuration
        
        returns:
            ModelTrainerConfig: the configuration for model trainer
        '''
        config = self.config.model_trainer
        params = self.params.train_arguments
        
        create_directories([config.root_dir])
        
        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            val_data_path=config.val_data_path,
            model_ckpt=config.model_ckpt,
            model_pickle=config.model_pickle,
            tokenizer_pickle=config.tokenizer_pickle,
            num_train_epochs=params.num_train_epochs,
            warmup_steps=params.warmup_steps,
            per_device_train_batch_size=params.per_device_train_batch_size,
            weight_decay=params.weight_decay,
            logging_steps=params.logging_steps,
            evaluation_strategy=params.evaluation_strategy,
            eval_steps=params.eval_steps,
            save_steps=params.save_steps,
            gradient_accumulation_steps=params.gradient_accumulation_steps
        )
        
        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        '''
        creates and returns model evaluation configuration
        
        returns:
            ModelEvaluationConfig: the configuration for model evaluation
        '''
        
        config = self.config.model_evaluation
        
        create_directories([config.root_dir])
        
        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_path=config.model_path,
            tokenizer_path=config.tokenizer_path,
            model_pkl=Path(config.model_pkl),
            tokenizer_pkl=Path(config.tokenizer_pkl),
            metric_file_name=config.metric_file_name
        )
        
        return model_evaluation_config
    
    def get_prediction_config(self) -> PredictionConfig:
        '''
        creates and returns model prediction configuration
        
        returns:
            PredictionConfig: the configuration for model prediction
        '''
        config = self.config.prediction
        
        model_prediction_config = PredictionConfig(
            model_path=config.model_path,
            tokenizer_path=config.tokenizer_path 
        )
        
        return model_prediction_config
    