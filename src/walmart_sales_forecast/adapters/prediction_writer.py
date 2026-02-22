import csv
from pathlib import Path


class PredictionCsvWriterAdapter:
    def save_predictions(self, predictions: list[float], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow(["weekly_sales_prediction"])
            for value in predictions:
                writer.writerow([round(value, 2)])
