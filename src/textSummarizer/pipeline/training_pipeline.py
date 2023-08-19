from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_ingestion import DataIngestion
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
            self.__data_ingestion()
            logger.info("STAGE -- Data Ingestion completed ---")
            
        except Exception as e:
            logger.exception(e)
            raise e 
        
        
    def __data_ingestion(self):
        '''
        initiates the data ingestion task under the training pipeline
        '''
        data_ingestion_config = self.config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()
        data_ingestion.extract_zip_data()
        