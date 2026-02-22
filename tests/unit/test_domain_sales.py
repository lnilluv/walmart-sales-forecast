import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from walmart_sales_forecast.domain.sales_rules import build_store_average_model, predict_with_store_average


class DomainSalesTests(unittest.TestCase):
    def test_build_store_average_model_uses_store_level_mean(self) -> None:
        rows = [
            {"Store": "1", "Weekly_Sales": "100.0"},
            {"Store": "1", "Weekly_Sales": "200.0"},
            {"Store": "2", "Weekly_Sales": "300.0"},
        ]

        model = build_store_average_model(rows)
        self.assertEqual(model["store_mean"]["1"], 150.0)
        self.assertEqual(model["global_mean"], 200.0)

    def test_predict_with_store_average_falls_back_to_global_mean(self) -> None:
        model = {"store_mean": {"1": 150.0}, "global_mean": 180.0}
        predictions = predict_with_store_average(model, [{"Store": "1"}, {"Store": "999"}])
        self.assertEqual(predictions, [150.0, 180.0])


if __name__ == "__main__":
    unittest.main()
