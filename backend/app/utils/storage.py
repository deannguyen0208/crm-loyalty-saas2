from pathlib import Path


def ensure_storage(path: str) -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output
