from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger


def make_sine_wave(
    filename: Path,
    a: float = 3,
    f: float = 2,
    t: np.ndarray = np.linspace(0, 4, 100),
    s: float = 0.2,
) -> None:
    if filename.exists():
        logger.info(f"Data already generated in {filename}")
    else:
        noise = np.random.normal(scale=s, size=len(t))
        v = a * np.sin(f * t) + noise
        pd.DataFrame({"time": t, "value": v}).to_csv(filename, index=False)
        logger.info(f"Data generated at {filename}.")
    return filename


def make_linear(
    filename: Path, size: int = 100, a: float = 2, b: float = 4, s: float = 0.5
):

    if filename.exists():
        logger.info(f"Data already generated in {filename}")
    else:
        x = np.linspace(0, 1, size)
        noise = np.random.normal(scale=s, size=len(x))
        y = a * x + b + noise
        pd.DataFrame({"x": x, "y": y}).to_csv(filename, index=False)
        logger.info(f"Data generated at {filename}.")
    return filename

def make_quadratic(
    filename: Path, size: int = 100, a: float = 3, b: float = 2.5, c=1.5, s: float = 0.5
):

    x = np.linspace(-2, 2, size)
    noise = np.random.normal(scale=s, size=len(x))
    y = a * x**2 + b * x + c + noise
    pd.DataFrame({"x": x, "y": y}).to_csv(filename, index=False)
    logger.info(f"Data generated at {filename}.")
    return filename