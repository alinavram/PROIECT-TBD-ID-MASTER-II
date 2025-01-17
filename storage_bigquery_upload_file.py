import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import os
import requests
from constants import *

# Seteaza calea catre fisierul de autentificare
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = JSON_KEY


def download_parquet_file(year, month, base_url, output_dir):
    month_str = f"{month:02d}"

    # Construieste URL-ul
    file_url = base_url.format(year=year, month=month_str)
    output_path = os.path.join(output_dir, f"yellow_tripdata_{year}-{month_str}.parquet")

    if os.path.exists(output_path):
        print(f"Fisierul {output_path} exista deja. Descarcarea nu este necesara.")
        return

    os.makedirs(output_dir, exist_ok=True)

    try:
        print(f"Descarc fisierul de la: {file_url}")

        # Trimite o cerere GET catre URL
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Verifica daca cererea a avut succes

        # Scrie continutul fisierului in output_path
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Fisierul a fost descarcat cu succes la: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Eroare la descarcarea fisierului de la {file_url}: {e}")


def preprocess_parquet(file_path, output_dir="Processed_files"):
    df = pd.read_parquet(file_path, engine='pyarrow')

    for column in df.columns:
        missing_ratio = df[column].isna().mean()
        if missing_ratio > 0.5:
            print(f"Elimin atributul {column} (mai mult de 50% date lipsa).")
            df = df.drop(columns=[column])
        elif missing_ratio <= 0.5:
            print(f"Elimin randurile lipsa pentru atributul {column}.")
            df = df.dropna(subset=[column])

    os.makedirs(output_dir, exist_ok=True)

    # Salvare fisier preprocesat local
    output_file = os.path.join(output_dir, f"processed_{os.path.basename(file_path)}")
    df.to_parquet(output_file)
    print(f"Fisierul preprocesat a fost salvat local la: {output_file}")

    return output_file


def create_bucket_if_not_exists(client, bucket_name, location="US"):
    try:
        bucket = client.get_bucket(bucket_name)
        print(f"Bucket-ul '{bucket_name}' exista deja.")
    except Exception as e:
        # Dacă bucket-ul nu există, îl creăm
        print(f"Bucket-ul '{bucket_name}' nu exista. Se creeaza acum.")
        bucket = client.bucket(bucket_name)
        bucket.location = location
        client.create_bucket(bucket)
        print(f"Bucket-ul '{bucket_name}' a fost creat cu succes in locatia '{location}'.")


def upload_parquet_to_storage(client, local_file_path, bucket_name, output_path):
    create_bucket_if_not_exists(client, bucket_name)

    file_name = os.path.basename(local_file_path)

    # Incarcă fisierul in bucket
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(output_path + file_name)
    blob.upload_from_filename(local_file_path)
    print(f"Fisierul {file_name} a fost incarcat in GCS la: {output_path}{file_name}")

    return f"gs://{bucket_name}/{output_path}{file_name}"


def create_dataset_if_not_exists(project_id, dataset_id):
    client = bigquery.Client(project=project_id)
    dataset_ref = f"{project_id}.{dataset_id}"

    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset-ul '{dataset_id}' exista deja.")
    except Exception as e:
        print(f"Creez dataset-ul '{dataset_id}'.")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset-ul '{dataset_id}' a fost creat.")


def import_parquet_to_bigquery(project_id, dataset_id, table_id, gcs_uri):
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()
    print(f"Datele din {gcs_uri} au fost incarcate in tabelul '{table_ref}'.")


# Creeaza un client pentru Google Cloud Storage
gcs_client = storage.Client(project=PROJECT_ID)

# 1. Descarcarea fisierului PARQUET
download_parquet_file(YEAR_TO_DOWNLOAD, MONTH_TO_DOWNLOAD, BASE_URL, OUTPUT_DIR)

# 2. Preprocesarea fisierului descarcat
file_path = os.path.join(OUTPUT_DIR, f"yellow_tripdata_{YEAR_TO_DOWNLOAD}-{MONTH_TO_DOWNLOAD:02d}.parquet")
processed_file_path = preprocess_parquet(file_path, PROCESSED_DIR)

# 3. Incarcarea fisierului preprocesat in Google Cloud Storage
gcs_uri = upload_parquet_to_storage(gcs_client, processed_file_path, BUCKET_NAME, OUTPUT_PATH_GCS)

# 4. Crearea dataset-ului in BigQuery (daca nu exista deja)
create_dataset_if_not_exists(PROJECT_ID, DATASET_ID)

# 5. Importul fisierului PARQUET in tabelul BigQuery
import_parquet_to_bigquery(PROJECT_ID, DATASET_ID, TABLE_ID, gcs_uri)
