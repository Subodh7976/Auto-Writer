from webScraper.entity import GoogleSearcherConfig
from webScraper.constants import API_KEY, CX

from googleapiclient.discovery import build
from datetime import date
import json 
import os 


class GoogleSearcher:
    def __init__(self, config: GoogleSearcherConfig):
        '''
        creates an instance for Google Searcher class for 
        getting searchable instances for query
        
        params:
            config: GoogleSearchConfig - configuration for google searcher
        '''
        self.config = config
        
    def search(self, query: str, num: int) -> dict:
        '''
        gather search results for given query available on google and saves it
        
        params:
            query: str - the searchable query
            num: int - number results to be extracted
        returns:
            dict: the results with requested query
        '''
        service = build(
            "customsearch", "v1", developerKey=API_KEY
        )
        
        res = (
            service.cse()
            .list(
                q=query,
                cx=CX,
                num=num
            )
            .execute()
        )
        
        results = list()
        for item in res['items']:
            results.append({
                "title": item['title'],
                "link": item['link']
            })
        
        save_path = os.path.join(self.config.record_path, str(date.today()))
        os.makedirs(
            save_path,
            exist_ok=True
        )
        
        content = {'query': query, 'results': results}
        with open(os.path.join(save_path, query+'.json'), 'w') as file:
            json.dump(content, file)
        
        return content