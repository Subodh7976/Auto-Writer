from webScraper.entity import TrendsScraperConfig

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
import json 
import os


class TrendsScraper:
    def __init__(self, config: TrendsScraperConfig):
        '''
        creates an instance for Trends Scraper class for 
        scraping daily trends from Google Trends
        
        params:
            config: TrendsScraperConfig - configuration for trends scraper
        '''
        self.config = config
        
    def get_trends(self) -> list:
        '''
        scrapes currently trending topics with attached article's urls
        
        returns:
            list: iterable containing trends
        '''
        client = urlopen(self.config.request_url)
        xml_page = client.read()
        client.close()
        
        soup = BeautifulSoup(xml_page, 'xml')
        items_list = soup.find_all('item')
        
        trend_list = list()
        for item in items_list:
            content = {'title': item.title.text}
            url_list = list()
            
            for news_item in item.find_all('ht:news_item'):
                url_list.append(
                    {
                        "source": news_item.find('ht:news_item_source').text,
                        "url": news_item.find("ht:news_item_url").text  
                    }
                )
            content['news'] = url_list
            trend_list.append(content)
            
        today = date.today()
        
        if os.path.exists(self.config.record_path):
            with open(self.config.record_path, 'r') as file:
                existing_record = json.load(file)
                
            for item in trend_list:
                if item['title'] not in existing_record['titles']:
                    existing_record['titles'].append(item['title'])
                    existing_record['trends'].append(
                        {
                            'title': item['title'],
                            'news': item['news'],
                            'date': str(today)
                        }
                    )
                else:
                    trend_list.remove(item) 
        else:
            titles = []
            trends = []
            for item in trend_list:
                titles.append(item['title'])
                trends.append(
                    {
                        'title': item['title'],
                        'news': item['news'],
                        'date': str(today) 
                    }
                )
            existing_record = {
                'titles': titles,
                'trends': trends
            }
            
        with open(self.config.record_path, 'w') as file:
            json.dump(existing_record, file)
            
        return trend_list