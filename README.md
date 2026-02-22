# Walmart Sales Forecast

Production-ready baseline forecasting project for Walmart weekly sales.

## Portfolio highlights

- Split from monorepo into a dedicated forecasting repository
- Refactored into hexagonal architecture for domain/app/adapter separation
- Added CLI workflow for training and prediction generation
- Added unit tests for forecasting rules and application use cases
- Added local smoke tests and Dockerized execution
- Added dependency vulnerability scan workflow (`pip-audit`)

## Project layout

- `src/walmart_sales_forecast/domain/`: sales forecasting rules
- `src/walmart_sales_forecast/application/`: use cases and ports
- `src/walmart_sales_forecast/adapters/`: CSV IO, model registry, prediction output
- `src/walmart_sales_forecast/bootstrap/`: CLI wiring
- `tests/unit/`: unit tests for domain and application layers
- `scripts/smoke_test.sh`: end-to-end train/predict smoke test
- `data/raw/`: source CSV

## Quick start

```bash
export PYTHONPATH=src
python3 -m unittest discover -s tests/unit -p 'test_*.py'
./scripts/smoke_test.sh
```

## CLI usage

```bash
python3 -m walmart_sales_forecast.bootstrap.cli train \
  --train-csv data/raw/Walmart_Store_sales.csv \
  --model-output artifacts/model.pkl

python3 -m walmart_sales_forecast.bootstrap.cli predict \
  --inference-csv data/raw/Walmart_Store_sales.csv \
  --model-path artifacts/model.pkl \
  --output-csv artifacts/predictions.csv
```

## Docker

```bash
docker build -t walmart-sales-forecast:local .
docker run --rm -v "$PWD/artifacts:/app/artifacts" walmart-sales-forecast:local \
  train --train-csv /app/data/raw/Walmart_Store_sales.csv --model-output /app/artifacts/model.pkl

docker run --rm -v "$PWD/artifacts:/app/artifacts" walmart-sales-forecast:local \
  predict --inference-csv /app/data/raw/Walmart_Store_sales.csv --model-path /app/artifacts/model.pkl --output-csv /app/artifacts/predictions.csv
```

## Verification commands

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py'
./scripts/smoke_test.sh
docker build -t walmart-sales-forecast:local .
```
