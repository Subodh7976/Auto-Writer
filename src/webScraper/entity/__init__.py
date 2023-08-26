from dataclasses import dataclass
from pathlib import Path 


@dataclass(frozen=True)
class TrendsScraperConfig:
    root_dir: Path 
    record_path: Path 
    request_url: str 
    

@dataclass(frozen=True)
class GoogleSearcherConfig:
    root_dir: Path 
    record_path: str
    

@dataclass(frozen=True)
class ArticleScraperConfig:
    root_dir: Path 
    record_path: str 