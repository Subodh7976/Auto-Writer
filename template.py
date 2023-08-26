import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

summarizer = "textSummarizer"
generator = "textGenerator"
scraper = "webScraper"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{summarizer}/__init__.py",
    f"src/{summarizer}/components/__init__.py",
    f"src/{generator}/__init__.py",
    f"src/{generator}/components/__init__.py",
    f"src/{scraper}/__init__.py",
    f"src/{scraper}/components/__init__.py",
    "src/utils/__init__.py",
    "src/utils/common.py",
    "src/logger/__init__.py",
    f"src/{summarizer}/config/__init__.py",
    f"src/{summarizer}/config/configuration.py",
    f"src/{summarizer}/pipeline/__init__.py",
    f"src/{summarizer}/entity/__init__.py",
    f"src/{summarizer}/constants/__init__.py",
    f"src/{scraper}/config/__init__.py",
    f"src/{scraper}/config/configuration.py",
    f"src/{scraper}/pipeline/__init__.py",
    f"src/{scraper}/entity/__init__.py",
    f"src/{scraper}/constants/__init__.py",
    f"src/{generator}/config/__init__.py",
    f"src/{generator}/config/configuration.py",
    f"src/{generator}/pipeline/__init__.py",
    f"src/{generator}/entity/__init__.py",
    f"src/{generator}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/generate.html",
    "templates/index.html"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass 
            logging.info(f"Creating empty file: {filepath}")
            
    else:
        logging.info(f"{filename} is already exists")