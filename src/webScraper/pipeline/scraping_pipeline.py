from webScraper.components.trends_scraper import TrendsScraper
from webScraper.components.google_searcher import GoogleSearcher
from webScraper.components.article_scraper import ArticleScraper
from webScraper.config.configuration import ConfigurationManager



class ScrapingPipeline:
    def __init__(self):
        '''
        initiates the scraping pipeline and loads the configuration
        '''
        self.config = ConfigurationManager()
        
    def scrape(self, scrape_num: int = 1, num: int = 5) -> list:
        '''
        scrapes the data by identifying the query for the 
        target article
        
        params:
            scrape_num: int - number of article to be scraped
            num: int - number of maximum results for google search
        returns:
            list: list of scraped results
        '''
        trend_scraper = TrendsScraper(self.config.get_trends_scraper_config())
        trends = trend_scraper.get_trends()
        
        if scrape_num < len(trends):
            trends = trends[:scrape_num]
        google_searcher = GoogleSearcher(self.config.get_google_searcher_config())
        article_scraper = ArticleScraper(self.config.get_article_scraper_config())
        
        scraped_results = []
        for trend in trends:
            search_results = google_searcher.search(trend['title'], num=num)
            search_results['results'].extend([
                {'title': i['source'], 'link': i['url']} for i in trend['news']
            ])
            
            scraped_trend = article_scraper.scrape(search_results)
            scraped_results.append(scraped_trend)
            
        return scraped_results