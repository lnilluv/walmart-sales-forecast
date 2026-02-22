import csv
from pathlib import Path


class SalesDatasetCsvAdapter:
    def load_training(self, csv_path: Path) -> list[dict]:
        with csv_path.open("r", encoding="utf-8", newline="") as file_handle:
            return list(csv.DictReader(file_handle))

    def load_inference(self, csv_path: Path) -> list[dict]:
        with csv_path.open("r", encoding="utf-8", newline="") as file_handle:
            return list(csv.DictReader(file_handle))
