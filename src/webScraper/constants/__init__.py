from pathlib import Path 
from decouple import config 

API_KEY = config('google_api_key')
CX = config('google_cx')
CONFIG_FILE_PATH = Path('config/config.yaml')
