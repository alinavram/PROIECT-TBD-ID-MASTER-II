# Configurari pentru descarcare si incarcare fisier
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet"
OUTPUT_DIR = "Parquet_files"
PROCESSED_DIR = "Processed_files"
BUCKET_NAME = "bucket-tbd-1"
OUTPUT_PATH_GCS = "preprocessed-data/"
PROJECT_ID = "tbd-master"
DATASET_ID = "nyc_taxi"
TABLE_ID = "tripdata"

# Anul si luna pentru fisierul de descarcat
YEAR_TO_DOWNLOAD = 2024
MONTH_TO_DOWNLOAD = 9

JSON_KEY = r"C:\Users\LENOVO\Desktop\Master2-Sem1\TBD\UserKey\tbd-master-c7ce81d7a7de.json"
