# weather-data-pipeline

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
- Loads raw data into BigQuery 
- flatten nested Json using dbt
- Builds staging, intermediate, and mart models
- Adds audit columns for pipeline tracking

## Technologies
- Python
- Google Cloud Storage
- BigQuery
- dbt Core

## Data Source
- OpenWeatherMao current weather API
Raw BigQuery table
demo.openweather_raw

## dbt Models
### Staging Model
stg_openweather
Cleans and flattens the raw OpenWeather JSON data

### Intermediate Model
int_weather_metrics
Adds reusable weather metrics and classifications.

### Mart Model
fct_weather_summary
Final analytics-ready table for reporting and dashboarding

## How to run
1. Add your OpenWeatherMap API key to the python ingestion script:
api_key = "...."

2. Run the python ingestion script.
 python weathermap.py

3. Run dbt transformations.
   cd weather_dbt
   dbt run
   dbt test
4. Generate dbt documentation.
   dbt docs generate
   dbt docs serve 

python weathermap.py   

## Project Goal
The goal of this project is to demonstrate a production-style data pipeline:
API -> GCS -> BigQuery Raw -> dbt Staging -> dbt Intermediate -> dbt mart
