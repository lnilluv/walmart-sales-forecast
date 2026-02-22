import argparse
from pathlib import Path

from walmart_sales_forecast.adapters.dataset_csv import SalesDatasetCsvAdapter
from walmart_sales_forecast.adapters.model_registry import PickleRegistryAdapter
from walmart_sales_forecast.adapters.model_rule_based import StoreAverageModelAdapter
from walmart_sales_forecast.adapters.prediction_writer import PredictionCsvWriterAdapter
from walmart_sales_forecast.application.use_cases import predict_from_csv, train_from_csv


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Walmart Sales Forecast CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("--train-csv", required=True)
    train_parser.add_argument("--model-output", required=True)

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("--inference-csv", required=True)
    predict_parser.add_argument("--model-path", required=True)
    predict_parser.add_argument("--output-csv", required=True)

    return parser


def main() -> None:
    args = _build_parser().parse_args()
    dataset_adapter = SalesDatasetCsvAdapter()
    model_adapter = StoreAverageModelAdapter()
    registry_adapter = PickleRegistryAdapter()

    if args.command == "train":
        train_from_csv(
            dataset_port=dataset_adapter,
            model_port=model_adapter,
            registry_port=registry_adapter,
            training_csv_path=Path(args.train_csv),
            model_output_path=Path(args.model_output),
        )
        print(f"Model saved to {args.model_output}")
        return

    predictions = predict_from_csv(
        dataset_port=dataset_adapter,
        model_port=model_adapter,
        registry_port=registry_adapter,
        inference_csv_path=Path(args.inference_csv),
        model_path=Path(args.model_path),
    )
    PredictionCsvWriterAdapter().save_predictions(predictions, Path(args.output_csv))
    print(f"Predictions saved to {args.output_csv}")


if __name__ == "__main__":
    main()
