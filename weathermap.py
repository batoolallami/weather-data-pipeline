from datetime import datetime,timezone
import requests
import json
from google.cloud import storage
from google.cloud import bigquery

#----------------------------------------------
# CONFIG
#----------------------------------------------
api_key="....."
city='london'
project_id="durable-tracer-494302-u0"
bucket_name="bucket-1-batool"
local_file="weather.json"
database_id="demo"
table_id="openweather_raw"
gcs_file="raw/openweather/weather_raw.json"


#--------------
#1. extract
#-----------------
def extract_weather(api_key,city):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)
    response.raise_for_status()
    return response.json()

#------------------------
#2. save raw file
#-----------------------
def save_raw_json(data,local_file):
    data["ingestion_timestamp"]=datetime.now(timezone.utc).isoformat()
    with open(local_file,"w") as f:
        f.write(json.dumps(data) + "\n")
    print(f"saved raw json to {local_file}")

#-----------------------------
#3. UPLOAD TO GCS
#-----------------------------
def upload_to_gcs(project_id,bucket_name,local_file,gcs_file):
    storage_client=storage.Client(project=project_id)
    bucket=storage_client.bucket(bucket_name)
    blob=bucket.blob(gcs_file)
    blob.upload_from_filename(local_file)
    print(f"Uploaded to gs://{bucket_name}/{gcs_file}")

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
    print(f"loaded data into biqquery table {table_ref}")

#----------------------
# ORCHESTRATOR
#----------------------
def main():
    weather_data=extract_weather(api_key,city)
    save_raw_json(weather_data,local_file)
    upload_to_gcs(
        project_id,bucket_name,local_file,gcs_file
    )
    load_to_bigquery(
        project_id,bucket_name,local_file,gcs_file,database_id,table_id)
    
if __name__== "__main__":
    main()


