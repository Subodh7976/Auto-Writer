from src.textSummarizer.pipeline.prediction_pipeline import PredictionPipeline
from src.textGenerator.pipeline.prediction_pipeline import GeneratorPredictionPipeline
from src.webScraper.pipeline.scraping_pipeline import ScrapingPipeline
from utils.common import check_model_exist

from flask import Flask, render_template, request
from datetime import date
import json 
import os 
import time 


class MyFlask(Flask):
    def run(self, host=None, port=None, debug=None, 
            load_dotenv=None, **kwargs):
        if not self.debug or os.getenv('WERZEUG_RUN_PATH') == 'true':
            with self.app_context():
                global summarizer, generator, scraper
                summarizer = PredictionPipeline()
                generator = GeneratorPredictionPipeline()
                scraper = ScrapingPipeline()
        super(MyFlask, self).run(host=host, port=port, debug=debug,
                                 load_dotenv=load_dotenv, **kwargs)
                

app = MyFlask(__name__)
summarizer = None 
generator = None 
scraper = None

DATA_SAVE_PATH = os.path.join('artifacts', 'articles')


def generate_json(raw_data):
    os.makedirs(os.path.join(DATA_SAVE_PATH, str(date.today())), exist_ok=True)
    for item in raw_data:
        for i in item['results']:
            summaries = list()
            for content in i['content']:
                if len(content) > 250:
                    summaries.append(summarizer.predict(content))
            if len(summaries) > 0:
                i['summaries'] = summaries
            else:
                item['results'].remove(i)

        item['generated'] = generator.predict(
            "Write an article on title: " + item['query']
        )
        
        with open(os.path.join(DATA_SAVE_PATH, str(date.today()), item['query']+'.json'), 'w') as file:
            json.dump(item, file)
    
            
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    global summarizer, generator
    if summarizer.model is None:    
        summarizer.load_model_tokenizer()
    if generator.model is None:
        generator.load_model_tokenizer()
        
    sum_exist = True if summarizer.model is not None else False 
    gen_exist = True if generator.model is not None else False
    
    if request.method == "GET":
        
        
        return render_template('generate.html',
                               sum_exist=sum_exist, 
                               gen_exist=gen_exist)
    else:
        start_time = time.time()
        
        scrape_num = int(request.form.get('num'))
        
        if sum_exist or gen_exist:
            scraped_data = scraper.scrape(scrape_num=scrape_num)
            generate_json(scraped_data)
        
        time_taken = time.time() - start_time
        return render_template('generate.html', 
                               sum_exist=sum_exist,
                               gen_exist=gen_exist,
                               time_taken=time_taken)
        

if __name__ == "__main__":
    app.run(host="0.0.0.0")
