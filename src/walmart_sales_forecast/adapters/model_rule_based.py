from walmart_sales_forecast.domain.sales_rules import build_store_average_model, predict_with_store_average


class StoreAverageModelAdapter:
    def train(self, rows: list[dict]) -> object:
        return build_store_average_model(rows)

    def predict(self, model: object, rows: list[dict]) -> list[float]:
        if not isinstance(model, dict):
            raise TypeError("Expected dictionary model payload")
        return predict_with_store_average(model, rows)
