from textSummarizer.pipeline.training_pipeline import TrainingPipeline
from textGenerator.pipeline.training_pipeline import GeneratorTrainingPipeline

import sys


GENERATOR_ARG = "gen"
SUMMARIZER_ARG = "sum"

args = sys.argv


if SUMMARIZER_ARG in args:
    train_pipe = TrainingPipeline()
    train_pipe.train()
elif GENERATOR_ARG in args:
    gen_train_pipe = GeneratorTrainingPipeline()
    gen_train_pipe.train()
else:
    train_pipe = TrainingPipeline()
    gen_train_pipe = GeneratorTrainingPipeline()
    
    train_pipe.train()
    gen_train_pipe.train()