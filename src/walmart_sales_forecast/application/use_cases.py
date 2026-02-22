from pathlib import Path

from walmart_sales_forecast.application.ports import DatasetPort, ModelPort, RegistryPort


def train_from_csv(
    dataset_port: DatasetPort,
    model_port: ModelPort,
    registry_port: RegistryPort,
    training_csv_path: Path,
    model_output_path: Path,
) -> None:
    rows = dataset_port.load_training(training_csv_path)
    model = model_port.train(rows)
    registry_port.save(model, model_output_path)


def predict_from_csv(
    dataset_port: DatasetPort,
    model_port: ModelPort,
    registry_port: RegistryPort,
    inference_csv_path: Path,
    model_path: Path,
) -> list[float]:
    rows = dataset_port.load_inference(inference_csv_path)
    model = registry_port.load(model_path)
    return model_port.predict(model, rows)
