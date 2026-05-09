# weather-data-pipeline

## Overview
This project is an end-to-end ETL/ELT pipeline using OpenWeatherMap API, Google Cloud Storage, BigQuery, and dbt.
This pipeline extracts weather data from external API, stores raw response in GCS, loads the raw data into BigQuery, and uses dbt to transform the data into clean analytics-ready models.

## Architecture
OpenWeatherMap API -> python extract script -> GCS raw landing zone -> BigQuery raw table -> dbt staging model
:arrow_down:


## Features
- API extraction
- Raw data storage
- BigQuery loading
- flatten nested Json

## Technologies
- Python
- Google Cloud Storage
- BigQuery
- dbt Core

## How to run
1. Add your API key:
```python
api_key = "...."
2. Run
python weathermap.py   
