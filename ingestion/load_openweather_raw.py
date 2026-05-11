import os
from dotenv import load_dotenv
from datetime import datetime,timezone
import requests
import json
from google.cloud import storage
from google.cloud import bigquery
import logging

load_dotenv()
api_key=os.getenv("OPENWEATHER_API_KEY")
project_id=os.getenv("PROJECT_ID")
bucket_name=os.getenv("BUCKET_NAME")
database_id=os.getenv("DATASET_ID")
table_id=os.getenv("TABLE_ID")
city=os.getenv("CITY")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getenv(
"GOOGLE_APPLICATION_CREDENTIALS"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_timestamp():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
#--------------
#1. extract
#-----------------
def extract_weather(api_key,city):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)
    response.raise_for_status()
    data= response.json()
    if not data:
        raise ValueError("API returned empty response")
    data["ingestion_timestamp"] =datetime.now(timezone.utc).isoformat()
    return data

#------------------------
#2. save raw file
#-----------------------
def save_raw_json(data,local_file):
    with open(local_file,"w") as f:
        f.write(json.dumps(data) + "\n")
    logging.info(f"saved raw json to {local_file}")

#-----------------------------
#3. UPLOAD TO GCS
#-----------------------------
def upload_to_gcs(project_id,bucket_name,local_file,gcs_file):
    storage_client=storage.Client(project=project_id)
    bucket=storage_client.bucket(bucket_name)
    blob=bucket.blob(gcs_file)
    blob.upload_from_filename(local_file)
    logging.info(f"Uploaded to gs://{bucket_name}/{gcs_file}")

#---------------------------
#4. LOAD TO BIGQUERY
#---------------------------
def load_to_bigquery(project_id,bucket_name,local_file,gcs_file,database_id,table_id):
    bq_client=bigquery.Client(project=project_id)
    uri=f"gs://{bucket_name}/{gcs_file}"
    job_config=bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    table_ref=f"{project_id}.{database_id}.{table_id}"
    load_job=bq_client.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config,
    )
    load_job.result()
    logging.info(f"loaded data into biqquery table {table_ref}")

#----------------------
# ORCHESTRATOR
#----------------------
def main():
    timestamp=get_timestamp()
    local_file=f"openweather_{timestamp}.json"
    gcs_file=f"raw/openweather/openweather_{timestamp}.json"
    weather_data=extract_weather(api_key,city)
    save_raw_json(weather_data,local_file)
    upload_to_gcs(
        project_id,bucket_name,local_file,gcs_file
    )
    load_to_bigquery(
        project_id,bucket_name,local_file,gcs_file,database_id,table_id)
    
if __name__== "__main__":
    try:
        main()
    except Exception:
        logging.error("ewather pipeline failed",exc_info=True)
        raise



