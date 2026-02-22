def build_store_average_model(rows: list[dict]) -> dict:
    by_store: dict[str, list[float]] = {}
    totals: list[float] = []

    for row in rows:
        if not row.get("Weekly_Sales"):
            continue
        store = str(row["Store"]).strip()
        sales = float(row["Weekly_Sales"])
        totals.append(sales)
        by_store.setdefault(store, []).append(sales)

    if not totals:
        return {"store_mean": {}, "global_mean": 0.0}

    store_mean = {store: sum(values) / len(values) for store, values in by_store.items()}
    global_mean = sum(totals) / len(totals)
    return {"store_mean": store_mean, "global_mean": global_mean}


def predict_with_store_average(model: dict, rows: list[dict]) -> list[float]:
    predictions: list[float] = []
    store_mean = model.get("store_mean", {})
    global_mean = float(model.get("global_mean", 0.0))

    for row in rows:
        store = str(row.get("Store", "")).strip()
        predictions.append(float(store_mean.get(store, global_mean)))
    return predictions
