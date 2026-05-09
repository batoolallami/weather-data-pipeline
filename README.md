# weather-data-pipeline

## Overview
This project is an end-to-end ETL/ELT pipeline using OpenWeatherMap API, Google Cloud Storage, BigQuery, and dbt.
This pipeline extracts weather data from external API, stores raw response in GCS, loads the raw data into BigQuery, and uses dbt to transform the data into clean analytics-ready models.

## Architecture
OpenWeatherMap API # weather-data-pipeline

## Overview
This project is an end-to-end ETL/ELT pipeline using OpenWeatherMap API, Google Cloud Storage, BigQuery, and dbt.
This pipeline extracts weather data from external API, stores raw response in GCS, loads the raw data into BigQuery, and uses dbt to transform the data into clean analytics-ready models.

## Architecture
OpenWeatherMap API 
       ↓ 
python extract script 
       ↓
GCS raw landing zone 
       ↓
BigQuery raw table
       ↓
dbt staging model
       ↓
dbt intermediate model
       ↓
dbt mart/final model
       ↓
Analytics / dashboards

## Features
- Extracts weather data from OpenWeatherMap API
- Stores raw JSON data in Google Cloud Storage
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
api_key = "...." python extract script -> GCS raw landing zone -> BigQuery raw table -> dbt staging model

2. Run
python weathermap.py   
