from textSummarizer.config.configuration import ConfigurationManager
from logger import logger
from utils.common import load_object

from pathlib import Path 
import pickle
import torch 
import os 


class PredictionPipeline:
    def __init__(self):
        '''
        initiates the prediction pipeline by loading in the model and tokenizer
        '''
        self.config = ConfigurationManager().get_prediction_config()
        self.model = None  
        self.tokenizer = None 
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model_tokenizer()
        
    def predict(self, input_batch, max_length=128):
        '''
        predicts the generated summary on given input batch
        
        params:
            input_batch - batch of the input data to be processed
            max_length: int - the maximum length of the generated summary
            
        returns:
            list: returns list of decoded summaries
        '''
        try:
            logger.info("STAGE --- Model Prediction started ---")
            inputs = self.tokenizer(input_batch, max_length=1024, truncation=True,
                                    padding="max_length", return_tensors="pt")
            summaries = self.model.generate(input_ids=inputs['input_ids'].to(self.device),
                                            attention_mask=inputs['attention_mask'].to(self.device),
                                            length_penalty=0.8, num_beams=8, max_length=max_length)
            
            decoded_summaries = [self.tokenizer.decode(summary, skip_special_tokens=True,
                                                       clean_up_tokenization_spaces=True) 
                                 for summary in summaries]
            logger.info("STAGE --- Model Prediction completed ---")
            
            return decoded_summaries
                        
        except Exception as e:
            logger.exception(e)
            raise e
        
    
    def load_model_tokenizer(self):
        '''
        loads the model and tokenizer if available
        '''
        self.model = load_object(Path(self.config.model_path))
        
        self.tokenizer = load_object(Path(self.config.tokenizer_path))
    