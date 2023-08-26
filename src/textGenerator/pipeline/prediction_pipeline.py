from textGenerator.config.configuration import ConfigurationManager
from logger import logger 

from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch 
import os 


class GeneratorPredictionPipeline:
    def __init__(self):
        '''
        initiates the prediction pipeline by loading in the model and tokenizer
        '''
        self.config = ConfigurationManager().get_prediction_configuration()
        self.model = None 
        self.tokenizer = None 
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def predict(self, prompt: str, max_length: int = 512):
        '''
        predicts the generated text on the given input prompt
        
        params:
            prompt: str - input prompt to be processed
            max_length: int - the maximum length of the output
            
        returns:
            list: returns list of generated text
        '''
        try:
            logger.info("STAGE --- Model Prediction started ---")
            self.model.eval()
            
            generated = torch.tensor(
                self.tokenizer.encode(prompt)
            ).unsqueeze(0)
            generated = generated.to(torch.device(self.device))
            
            sample_outputs = self.model.generate(
                generated,
                do_sample=True,
                top_k=50,
                max_length=max_length,
                top_p=0.95,
                num_return_sequences=5
            )
            
            decoded_text = [
                self.tokenizer.decode(i, skip_special_tokens=True) 
                for i in sample_outputs
            ]
            
            return decoded_text
            
        except Exception as e:
            logger.exception(e)
            raise e 
        
    def load_model_tokenizer(self):
        '''
        loads the model and tokenizer
        '''
        if os.path.exists(self.config.model_path):
            self.model = GPT2LMHeadModel.from_pretrained(
                self.config.model_path
            )
            self.tokenizer = GPT2Tokenizer.from_pretrained(
                self.config.model_path
            )
            
            self.model.to(self.device)
        