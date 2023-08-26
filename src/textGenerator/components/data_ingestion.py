import os 
import gdown 
from pathlib import Path 

from logger import logger 
from utils.common import get_size, create_directories
from textGenerator.config.configuration import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        '''
        create an instance for Data Ingestion class for 
        all the data ingestion techniques
        
        params:
            config: DataIngestionConfig - configuration for data ingestion
        '''
        self.config = config 
        
    def download_data(self):
        '''
        downloads the data if not already downloaded
        from Google Drive
        '''
        if not os.path.exists(self.config.local_data_file):
            filename = gdown.download(self.config.source_url,
                                      self.config.local_data_file)
            logger.info(f"{filename} downloaded!")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
            
