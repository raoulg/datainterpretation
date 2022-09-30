from pathlib import Path
from typing import List, Tuple

from pydantic import BaseModel


class Settings(BaseModel):
    imagedir: Path = Path("reports/img")
    mu: List[float] = [0.0, 10.0]
    sd: List[float] = [1.0, 1.0]
    figsize: Tuple = (10, 10)
    groups: int = 5
    difference: float = 0.2
    slope: float = 2
    var: float = 0.3
    n: int = 30
    pairs: List[Tuple] = [
        (1, 2),
        (2, 2),
        (2, 8),
        (2, 15),
        (2, 25),
        (2, 50),
    ]
    subs: Tuple = (2, 3)


presets = Settings()


class Models(BaseModel):
    processed_dir: Path = Path("./data/processed")
    target: str = "species"


modelsettings = Models()
