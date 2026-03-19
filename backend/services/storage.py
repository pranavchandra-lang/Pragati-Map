"""
Thread-safe JSON storage — all reads/writes go through here.
Prevents file corruption under concurrent FastAPI requests.
"""
import os
import json
import threading
from pathlib import Path

_lock = threading.Lock()
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))


def read_json(filename: str) -> dict:
    with _lock:
        path = DATA_DIR / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)


def write_json(filename: str, data: dict) -> None:
    with _lock:
        path = DATA_DIR / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
