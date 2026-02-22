FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY data/raw/Walmart_Store_sales.csv data/raw/Walmart_Store_sales.csv

USER appuser

ENTRYPOINT ["python", "-m", "walmart_sales_forecast.bootstrap.cli"]
