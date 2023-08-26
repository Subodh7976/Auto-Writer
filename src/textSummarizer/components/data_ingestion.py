import os
import gdown
from zipfile import ZipFile 
from pathlib import Path

from logger import logger 
from utils.common import get_size, create_directories
from textSummarizer.config.configuration import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        '''
        create an instance for Data Ingestion class
        
        params:
            config: DataIngestionConfig - configuration of data ingestion
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

    def extract_zip_data(self):
        '''
        extracts the data zip file 
        '''
        create_directories([self.config.unzip_dir])
        with ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.unzip_dir)
            
        logger.info(f"extracted data in {self.config.unzip_dir} path")
            