from textGenerator.config.configuration import DataTransformationConfig

from transformers import GPT2Tokenizer
import pandas as pd
from datasets import load_dataset, Dataset
from itertools import chain


class DataTransformation:
    def __init__(self, config: DataTransformationConfig, feature: str = "text"):
        '''
        creates an instance for Data Transformation class it 
        transforms the input unstructured data to tokens and numbers
        
        params:
            config: DataTransformationConfig - configuration for Data Transformation
            feature: str - the column feature to be used in the transformation
        '''
        self.config = config
        self.feature = feature

    def convert(self):
        '''
        reads the dataset from local disk, transforms the data to tokens and 
        stores the transformed data tensors in local disk
        '''
        overwrite_cache = False
        dataset = self.prepare_data()
        column_names = dataset['train'].column_names
        
        tokenizer = GPT2Tokenizer.from_pretrained(
            self.config.tokenizer_name,
            bos_token="<|startoftext|>",
            eos_token="<|endoftext|>",
            pad_token="<|pad|>"
        )
        
        preprocessing_num_worker = None
        
        tokenized_dataset = dataset.map(
            lambda x: tokenizer(x[self.feature], truncation=True),
            batched=True,
            num_proc=preprocessing_num_worker,
            remove_columns=column_names,
            desc="Running tokenizer on dataset"
        )
        
        lm_dataset = tokenized_dataset.map(
            self.__group_texts,
            batched=True,
            num_proc=preprocessing_num_worker,
            load_from_cache_file=not overwrite_cache,
            desc=f"Grouping texts in chunks of {self.config.block_size}"
        )
        
        lm_dataset.save_to_disk(
            self.config.save_data_path
        )
        
        
    def __group_texts(self, examples):
        concatenated_examples = {k: list(chain(*examples[k])) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        
        if total_length >= self.config.block_size:
            total_length = (total_length // self.config.block_size) * self.config.block_size
            
        result = {
            k: [t[i:i+self.config.block_size] for i in range(0, total_length, self.config.block_size)] 
            for k, t in concatenated_examples.items()
        }
        result['labels'] = result['input_ids'].copy()
        return result
        

    def prepare_data(self) -> Dataset:
        '''
        prepares the dataset by loading the csv file and into dataset class,
        also prepares the train and validation of the dataset
        
        returns: 
            Dataset: the splitted and loaded dataset
        '''
        data_files = {'train': self.config.local_data_path}
        validation_per = 5
        dataset_args = {}
        
        raw_dataset = load_dataset(
            'csv',
            sep=',',
            data_files=data_files
        )
        
        raw_dataset["validation"] = load_dataset(
            'csv',
            sep=',',
            data_files=data_files,
            split=f"train[:{validation_per}%]",
            **dataset_args
        )
        
        raw_dataset['train'] = load_dataset(
            'csv',
            sep=',',
            data_files=data_files,
            split=f"train[{validation_per}%:]",
            **dataset_args
        )
        
        return raw_dataset
        