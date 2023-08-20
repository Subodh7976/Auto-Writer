from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq, AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import load_from_disk
import torch 
import os 
import pickle 

from textSummarizer.config.configuration import ModelTrainerConfig


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
        trains the model over the specified arguments and saves the model 
        in local disk
        '''
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
        
        dataset_train = load_from_disk(
            self.config.train_data_path
        )
        dataset_val = load_from_disk(
            self.config.val_data_path
        )
        
        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=self.config.num_train_epochs, warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.per_device_train_batch_size, per_device_eval_batch_size=self.config.per_device_train_batch_size,
            weight_decay=self.config.weight_decay, logging_steps=self.config.logging_steps, 
            evaluation_strategy=self.config.evaluation_strategy, eval_steps=self.config.eval_steps, save_steps=self.config.save_steps,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps
        )
        
        trainer = Trainer(model=model, args=trainer_args,
                          tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                          train_dataset=dataset_train,
                          eval_dataset=dataset_val)
        
        trainer.train()
        
        model.save_pretrained(os.path.join(self.config.root_dir, "model_t5"))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer_t5"))
        
        with open(self.config.model_pickle, 'wb') as file:
            pickle.dump(model, file)
        
        with open(self.config.tokenizer_pickle, 'wb') as file:
            pickle.dump(tokenizer, file)
        