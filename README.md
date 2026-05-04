# weather-data-pipeline

## Overview
This project extracts weather data from OpenWeatherMap API, stores raw JSON in GCS, and loads it into BigQuery.

## Architecture
API -> JSON -> GCS -> BigQuery

## Features
- API extraction
- Raw data storage
- BigQuery loading
- flatten nested Json

## Technologies
- Python
- Google Cloud Storage
- BigQuery

## How to run
1. Add your API key:
```python
api_key = "...."
2. Run
python weathermap.py   
