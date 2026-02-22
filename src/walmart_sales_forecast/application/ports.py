from pathlib import Path
from typing import Protocol


class DatasetPort(Protocol):
    def load_training(self, csv_path: Path) -> list[dict]: ...

    def load_inference(self, csv_path: Path) -> list[dict]: ...


class ModelPort(Protocol):
    def train(self, rows: list[dict]) -> object: ...

    def predict(self, model: object, rows: list[dict]) -> list[float]: ...


class RegistryPort(Protocol):
    def save(self, model: object, path: Path) -> None: ...

    def load(self, path: Path) -> object: ...
