from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch 
import pandas as pd 
from tqdm import tqdm

from textSummarizer.config.configuration import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        '''
        create an instance for Model Evaluation class
        which evaluates the model on different metric
        
        returns:
            ModelEvaluationConfig: the configuration for model evaluation
        '''
        self.config = config
        
    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        '''
        split the dataset into smaller batches that can be processed simultaneously
        
        params:
            list_of_elements: list - elements to converted into batches
            batch_size: int - the size of batch to be formed
        '''
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i+batch_size]
            
    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer,
                                    batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
                                    column_text="article",
                                    column_summary="highlights"):
        '''
        calculates metrics on the input dataset over a given metric
        
        params:
            dataset:  - dataset which will be evaluated
            metric:  - metric which will be used for the evaluation
            model:  - the model which will be evaluated
            tokenizer:  - the tokenizer to tokenize the dataset
            batch_size: int - the size of the batch to be evaluated
            device: str - the device which will be used by the model
            column_text: str - the feature in the dataset to be used as input
            column_summary: str - the feature in the dataset to be used as target
        '''
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))
        
        for article_batch, target_batch in tqdm(
            zip(article_batch, target_batch), total=len(article_batches)
        ):
            inputs = tokenizer(article_batch, max_length=1024, truncation=True,
                               padding="max_length", return_tensors='pt')
            summaries = model.generate(input_ids=inputs['input_ids'].to(device),
                                       attention_mask=inputs['attention_mask'].to(device),
                                       length_penalty=0.8, num_beans=8, max_length=128)
            
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                                  clean_up_tokenization_spaces=True) for s in summaries]
            
            metric.add_batch(predictions=decoded_summaries, references=target_batch)
            
        score = metric.compute()
        return score 
    
    def evaluate(self):
        '''
        evaluates the test dataset on multiple rouge metrics and 
        saves metric to csv
        '''
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
        
        dataset_test = pd.read_csv(self.config.data_path)
        
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        
        rouge_metric = load_metric('rogue')
        
        score = self.calculate_metric_on_test_ds(
            dataset_test[0:10], rouge_metric, model, tokenizer, 
            batch_size=2, column_text="article", column_summary="highlights"
        )
        
        rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)
        
        df = pd.DataFrame(rouge_dict, index=['pegasus'])
        df.to_csv(self.config.metric_file_name, index=False)
        