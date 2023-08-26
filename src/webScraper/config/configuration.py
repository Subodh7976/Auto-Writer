from webScraper.constants import *
from webScraper.entity import (
    TrendsScraperConfig,
    GoogleSearcherConfig,
    ArticleScraperConfig
)
from utils.common import read_yaml, create_directories

from pathlib import Path 


class ConfigurationManager:
    def __init__(self,
                 config_filepath: Path = CONFIG_FILE_PATH):
        '''
        creates a configuration manager class which manages configuration 
        for various stages of development
        
        params:
            config_filepath: Path - configuration yaml file path
        '''
        self.config = read_yaml(config_filepath)
        self.config = self.config.web_scraper
        
        create_directories([self.config.artifacts_root])
        
    def get_trends_scraper_config(self) -> TrendsScraperConfig:
        '''
        creates and returns trends scraper configuration
        
        returns:
            TrendsScraperConfig: the configuration for trends scraper
        '''
        config = self.config.trends_scraper
        
        create_directories([config.root_dir])
        
        trends_scraper_config = TrendsScraperConfig(
            root_dir=config.root_dir,
            record_path=config.record_path,
            request_url=config.request_url
        )
        
        return trends_scraper_config
    
    def get_google_searcher_config(self) -> GoogleSearcherConfig:
        '''
        creates and returns google searches configuration
        
        returns:
            GoogleSearcherConfig: the configuration for google searcher
        '''
        config = self.config.google_searcher
        
        create_directories([config.root_dir])
        
        google_searcher_config = GoogleSearcherConfig(
            root_dir=config.root_dir,
            record_path=config.record_path
        )
        
        return google_searcher_config
    
    def get_article_scraper_config(self) -> ArticleScraperConfig:
        '''
        creates and returns article scraper configuration
        
        returns:
            ArticleScraperConfig: the configuration for article scraper
        '''
        config = self.config.article_scraper
        
        create_directories([config.root_dir])
        
        article_scraper_config = ArticleScraperConfig(
            root_dir=config.root_dir,
            record_path=config.record_path
        )
        
        return article_scraper_config
    