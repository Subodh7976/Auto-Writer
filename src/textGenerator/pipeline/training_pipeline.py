from textGenerator.config.configuration import ConfigurationManager
from textGenerator.components.data_ingestion import DataIngestion
from textGenerator.components.data_transformation import DataTransformation
from textGenerator.components.data_validation import DataValidation
from textGenerator.components.model_trainer import ModelTrainer
from logger import logger 


class GeneratorTrainingPipeline:
    def __init__(self):
        '''
        creates an instance of the Text Generator model
        training pipeline
        '''
        self.config = ConfigurationManager()
        
    def train(self):
        '''
        initiates the training of the text generator model
        '''
        try:
            logger.info("STAGE --- Data Ingestion started ---")
            self.data_ingestion()
            logger.info("STAGE --- Data Ingestion completed ---")
            
            logger.info("STAGE --- Data Validation started ---")
            self.data_validation()
            logger.info("STAGE --- Data Validation completed ---")
            
            logger.info("STAGE --- Data Transformation started ---")
            self.data_transformation()
            logger.info("STAGE --- Data Transformation completed ---")
            
            logger.info("STAGE --- Model Trainer started ---")
            self.model_trainer()
            logger.info("STAGE --- Model Trainer completed ---")
        
        except Exception as e:
            logger.exception(e)
            raise e 
        
    def data_ingestion(self):
        '''
        initiates the data ingestion task under the training pipeline
        '''
        data_ingestion_config = self.config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()

    def data_validation(self):
        '''
        initiates the data ingestion task under the training pipeline
        '''
        data_validation_config = self.config.get_data_validation_configuration()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_data()
        
    def data_transformation(self):
        '''
        initiates the data transformation task under the training pipeline
        '''
        data_transformation_config = self.config.get_data_transformation_configuration()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()
        
    def model_trainer(self):
        '''
        initiates the model training task under the training pipeline
        '''
        model_trainer_config = self.config.get_model_trainer_configuration()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()