# Market Data Service

A Python service for consuming market data, monitoring data freshness, and exposing health and metrics endpoints.

## Features

- Market data ingestion
- Stale data detection
- Health endpoint
- Prometheus metrics
- Logging
- Docker support

## Requirements

- Python 3.11+
- uv
- Docker (optional)

## Run Locally

Install dependencies:

    uv sync

Start the service:

    uv run market-data-service

The service runs on port `8000`.

Check the health endpoint:

    curl localhost:8000/health

View metrics:

    curl localhost:8000/metrics

## Run with Docker

Build the image:

    docker build -t market-data-service .

Run the container:

    docker run --rm -p 8000:8000 market-data-service

Check the health endpoint:

    curl localhost:8000/health

View metrics:

    curl localhost:8000/metrics

View container logs:

    docker logs <container-name>

## Tests

Run the test suite:

    uv run pytest

## Project Structure

    market-data-service/
    ├── src/
    │   └── market_data_service/
    ├── tests/
    ├── .github/
    ├── pyproject.toml
    ├── uv.lock
    ├── Dockerfile
    └── README.md

## Future Improvements

- Add Docker health checks
- Run the container as a non-root user
- Expand monitoring and alerting
- Add Docker build and smoke tests to CI
