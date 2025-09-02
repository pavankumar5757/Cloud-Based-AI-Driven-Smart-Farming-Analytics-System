import os
import pickle
from typing import Any

model_cache = {}

def save_model(model: Any, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_model(path: str) -> Any:
    with open(path, "rb") as f:
        return pickle.load(f)

