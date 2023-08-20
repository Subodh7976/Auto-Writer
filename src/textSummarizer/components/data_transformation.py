from textSummarizer.config.configuration import DataTransformationConfig

from transformers import AutoTokenizer
import pandas as pd
from datasets import Dataset
import os 


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        '''
        creates an instance for Data Transformation class 
        it transforms the input unstructured data to tokens and 
        numbers
        
        params:
            config: DataTransformationConfig - configuration for Data Transformation
        '''
        self.config = config 
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)
        
    def convert_examples_to_features(self, example_batch):
        '''
        converts a batch of input unstructured text data to 
        tokenized and transformed, numerical data
        
        params:
            example_batch - a batch of examples
        returns:
            dict - a dictionary containing input ids, attention mask and labels
        '''
        input_encodings = self.tokenizer(
            example_batch['article'], max_length=1024, truncation=True 
        )
        
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(
                example_batch['highlights'], max_length=256, truncation=True 
            )
        
        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }
        
    def convert(self):
        '''
        reads the dataset from local disk, transforms the data to tokens
        and stores the transformed data tensors in local disk
        '''
        df = pd.read_csv(
            os.path.join(self.config.data_path, 'train.csv')
        )
        df = df.drop(['id'], axis=1)
        df_val = pd.read_csv(
            os.path.join(self.config.data_path, 'validation.csv')
        )
        
        dataset = Dataset.from_pandas(df.sample(150000))
        dataset_pt = dataset.map(self.convert_examples_to_features, batched=True)
        dataset_pt.save_to_disk(self.config.train_dataset)
        
        dataset_val = Dataset.from_pandas(df_val)
        dataset_val_pt = dataset_val.map(self.convert_examples_to_features, batched=True)
        dataset_val_pt.save_to_disk(self.config.val_dataset)
        