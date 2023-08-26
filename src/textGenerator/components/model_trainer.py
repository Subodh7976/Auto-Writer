from transformers import (
    GPT2Config,
    GPT2Tokenizer,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    default_data_collator
)
from datasets import load_from_disk
import torch 
import os 
import random
import numpy as np

from textGenerator.config.configuration import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        '''
        create an instance for Model Trainer class 
        which trains the model
        
        params:
            config: ModelTrainerConfig - configuration of model trainer
        '''
        self.config = config
        
    def train(self):
        '''
        trains the model over the specified arguments and saves the model in 
        local disk
        '''
        config = self.config
        tokenizer = GPT2Tokenizer.from_pretrained(
            config.model_name,
            bos_token="<|startoftext|>",
            eos_token="<|endoftext|>",
            pad_token="<|pad|>"
        )
        
        tokenized_dataset = load_from_disk(self.config.data_path)
        
        configuration = GPT2Config.from_pretrained(
            config.model_name,
            output_hidden_states=config.output_hidden_states
        )
        
        model = GPT2LMHeadModel.from_pretrained(
            config.model_name,
            config=configuration
        )
        
        model.resize_token_embeddings(len(tokenizer))
        
        if torch.cuda.is_available():
            device = "cuda"
            model.cuda()
            
        seed_val = 42
        random.seed(seed_val)
        np.random.seed(seed_val)
        torch.manual_seed(seed_val)
        torch.cuda.manual_seed_all(seed_val)
        
        train_dataset = tokenized_dataset['train']
        eval_dataset = tokenized_dataset['validation']
        
        training_args = TrainingArguments(
            output_dir=config.output_dir,
            overwrite_output_dir=config.overwrite_output_dir,
            evaluation_strategy=config.evaluation_strategy,
            save_strategy=config.save_strategy
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            data_collator=default_data_collator,
            compute_metrics=config.compute_metrics,
            preprocess_logits_for_metrics=config.preprocess_logits_for_metrics
        )
        
        train_result = trainer.train(
            resume_from_checkpoint=config.resume_from_checkpoint
        )
        
        trainer.save_model(output_dir=config.output_dir)
        metrics = train_result.metrics
        trainer.save_metrics('train', metrics)
        trainer.save_state()
        