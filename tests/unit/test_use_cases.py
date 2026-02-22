import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from walmart_sales_forecast.application.ports import DatasetPort, ModelPort, RegistryPort
from walmart_sales_forecast.application.use_cases import predict_from_csv, train_from_csv


class FakeDatasetAdapter(DatasetPort):
    def load_training(self, csv_path: Path) -> list[dict]:
        return [{"Store": "1", "Weekly_Sales": "100"}]

    def load_inference(self, csv_path: Path) -> list[dict]:
        return [{"Store": "1"}]


class FakeModelAdapter(ModelPort):
    def train(self, rows: list[dict]) -> object:
        return {"global_mean": 100.0, "store_mean": {"1": 100.0}}

    def predict(self, model: object, rows: list[dict]) -> list[float]:
        return [100.0]


class FakeRegistryAdapter(RegistryPort):
    def __init__(self) -> None:
        self.saved = False
        self.loaded = False

    def save(self, model: object, path: Path) -> None:
        self.saved = True

    def load(self, path: Path) -> object:
        self.loaded = True
        return {"global_mean": 100.0, "store_mean": {"1": 100.0}}


class UseCaseTests(unittest.TestCase):
    def test_train_from_csv_saves_model(self) -> None:
        dataset = FakeDatasetAdapter()
        model = FakeModelAdapter()
        registry = FakeRegistryAdapter()
        train_from_csv(dataset, model, registry, Path("train.csv"), Path("model.pkl"))
        self.assertTrue(registry.saved)

    def test_predict_from_csv_loads_model(self) -> None:
        dataset = FakeDatasetAdapter()
        model = FakeModelAdapter()
        registry = FakeRegistryAdapter()
        predictions = predict_from_csv(dataset, model, registry, Path("predict.csv"), Path("model.pkl"))
        self.assertTrue(registry.loaded)
        self.assertEqual(predictions, [100.0])


if __name__ == "__main__":
    unittest.main()
