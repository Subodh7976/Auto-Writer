from textGenerator.constants import *
from utils.common import read_yaml, create_directories
from textGenerator.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    PredictionConfig
)

from pathlib import Path


class ConfigurationManager:
    def __init__(self,
                 config_filepath: Path = CONFIG_FILE_PATH,
                 params_filepath: Path = PARAMS_FILE_PATH):
        '''
        create a configuration manager class which manages configuration for 
        various stages of development
        
        params:
            config_filepath: Path - configuration yaml file path
            params_filepath: Path - parameters yaml file path
        '''
        self.config = read_yaml(config_filepath).text_generator
        self.params = read_yaml(params_filepath).text_generator
        
    
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
            local_data_file=config.local_data_file
        )
 
        return data_ingestion_config
        
    def get_data_validation_configuration(self) -> DataValidationConfig:
        '''
        creates and returns data validation configuration
        
        returns:
            DataValidationConfig: the configuration for data validation
        '''
        config = self.config.data_validation
        
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir, 
            status_file=config.status_file,
            required_file=config.required_file
        )
        
        return data_validation_config
        
    def get_data_transformation_configuration(self) -> DataTransformationConfig:
        '''
        creates and returns data transformation configuration
        
        returns:
            DataTransformationConfig: the configuration for data transformation
        '''
        config = self.config.data_transformation
        
        create_directories([config.root_dir])
        
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            local_data_path=config.local_data_path,
            save_data_path=config.save_data_path,
            tokenizer_name=config.tokenizer_name,
            block_size=config.block_size
        )
        
        return data_transformation_config
    
    def get_model_trainer_configuration(self) -> ModelTrainerConfig:
        '''
        creates and returns model trainer configuration
        
        returns:
            ModelTrainerConfig: the configuration for model training
        '''
        config = self.config.model_trainer
        params = self.params.train_arguments
        
        create_directories([config.root_dir])
        
        
        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            output_dir=config.output_dir,
            data_path=config.data_path,
            model_name=config.model_name,
            output_hidden_states=params.output_hidden_states,
            overwrite_output_dir=params.overwrite_output_dir,
            evaluation_strategy=params.evaluation_strategy,
            save_strategy=params.save_strategy,
            compute_metrics=params.compute_metrics,
            preprocess_logits_for_metrics=params.preprocess_logits_for_metrics,
            resume_from_checkpoint=None
        )
        
        return model_trainer_config
    
    def get_prediction_configuration(self) -> PredictionConfig:
        '''
        creates and returns prediction configuration
        
        returns:
            PredictionConfig: the configuration for model prediction
        '''
        config = self.config.prediction
        
        prediction_config = PredictionConfig(
            model_path=config.model_path,
            model_name=config.model_name
        )
        
        return prediction_config
    