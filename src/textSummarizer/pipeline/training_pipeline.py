from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_ingestion import DataIngestion
from textSummarizer.components.data_validation import DataValidation
from textSummarizer.components.data_transformation import DataTransformation
from textSummarizer.components.model_trainer import ModelTrainer
from textSummarizer.components.model_evaluation import ModelEvaluation
from textSummarizer.logging import logger 


class TrainingPipeline:
    def __init__(self):
        '''
        Creates an instance of the Text Summarization model 
        training pipeline
       
        params:
            None 
        '''
        self.config = ConfigurationManager()
        
    def train(self):
        '''
        initiates the training of the text summarization model
        '''
        try:
            logger.info("STAGE --- Data Ingestion started ---")
            self.data_ingestion()
            logger.info("STAGE -- Data Ingestion completed ---")
            
            logger.info("STAGE --- data validation started ---")
            self.data_validation()
            logger.info("STAGE --- data validation completed ---")
            
            logger.info("STAGE --- data transformation started ---")
            self.data_transformation()
            logger.info("STAGE --- data transformation completed ---")
            
            logger.info("STAGE --- Model Trainer started ---")
            self.model_trainer()
            logger.info("STAGE --- Model Trainer completed ---")
            
            logger.info("STAGE --- Model Evaluation started ---")
            self.model_evaluation()
            logger.info("STAGE --- Model Evaluation completed ---")
            
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
        data_ingestion.extract_zip_data()
        
    def data_validation(self):
        '''
        initiates the data validation task under the training pipeline
        '''
        data_validation_config = self.config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_files()

    def data_transformation(self):
        '''
        initiates the data transformation task under the training pipeline
        '''
        data_transformation_config = self.config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()
    
    def model_trainer(self):
        '''
        initiates the model training task under the training pipeline
        '''
        model_trainer_config = self.config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()
    
    def model_evaluation(self):
        '''
        initiates the model evaluation task under the training pipeline
        '''
        model_evaluation_config = self.config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()
    