from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)


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
        self.params = read_yaml(params_filepath)
        
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
            tokenizer_name=config.tokenizer_name 
        )
        
        return data_transformation_config
    