#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT_DIR/src"

mkdir -p "$ROOT_DIR/artifacts"

python3 -m walmart_sales_forecast.bootstrap.cli train \
  --train-csv "$ROOT_DIR/data/raw/Walmart_Store_sales.csv" \
  --model-output "$ROOT_DIR/artifacts/model.pkl"

python3 -m walmart_sales_forecast.bootstrap.cli predict \
  --inference-csv "$ROOT_DIR/data/raw/Walmart_Store_sales.csv" \
  --model-path "$ROOT_DIR/artifacts/model.pkl" \
  --output-csv "$ROOT_DIR/artifacts/predictions.csv"

ROOT_DIR_ENV="$ROOT_DIR" python3 - <<'PY'
import os
from pathlib import Path

output_path = Path(os.environ["ROOT_DIR_ENV"]) / "artifacts" / "predictions.csv"
if not output_path.exists():
    raise SystemExit("Missing predictions.csv")

line_count = sum(1 for _ in output_path.open("r", encoding="utf-8"))
if line_count < 2:
    raise SystemExit("Predictions file is unexpectedly empty")
print(f"Smoke test OK: {line_count - 1} predictions")
PY
