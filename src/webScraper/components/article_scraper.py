from webScraper.entity import ArticleScraperConfig

from bs4 import BeautifulSoup
from datetime import date
import threading
import requests
import json 
import os 


class ArticleScraper:
    def __init__(self, config: ArticleScraperConfig):
        '''
        create an instance for Article Scraper class for all the 
        article scraping tasks
        
        params:
            config: ArticleScraperConfig - configuration for article scraper
        '''
        self.config = config
        
    def scrape(self, results: dict) -> dict:
        '''
        scrapes the articles from the give results
        
        params:
            results: dict - dictionary containing results for any query
        returns:
            dict: dictionary containing scraped text for each result
        '''
        scraped_result = list()
        
        def execute_with_timeout(func, args=(), timeout=10):
            result = None 
            
            def worker():
                nonlocal result 
                result = func(args)
                
            thread = threading.Thread(target=worker)
            thread.start()
            thread.join(timeout)
            
            if thread.is_alive():
                return None 
            else:
                return result
            
        def get_text(url):
            return requests.get(url).text 
        
        
        for item in results['results']:
            scrape_text = execute_with_timeout(get_text, 
                                               (item['link']))
            if scrape_text is not None:
                soup = BeautifulSoup(scrape_text, 'html.parser')
                contents = [i.text for i in soup.find_all('p')]
                
                scraped_result.append({
                    'title': item['title'],
                    'link': item['link'],
                    'content': contents
                })
             
        save_path = os.path.join(self.config.record_path, str(date.today()))   
        os.makedirs(
            save_path,
            exist_ok=True 
        )
        
        content = {'query': results['query'], 'results': scraped_result}
        with open(os.path.join(save_path, results['query']+'.json'), 'w') as file:
            json.dump(content, file)
            
        return content 
