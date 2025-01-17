from google.cloud import bigquery
import os
from constants import JSON_KEY

# Seteaza calea catre fisierul de autentificare
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = JSON_KEY

# Creează un client BigQuery
client = bigquery.Client()

# Lista query-urilor
queries = {
    "filter_data": """
        CREATE OR REPLACE TABLE `tbd-master.nyc_taxi.filtered_tripdata` AS
        SELECT 
          trip_distance,
          PULocationID,
          DOLocationID,
          EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
          EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS pickup_day_of_week,
          TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, MINUTE) AS trip_duration_minutes,
          fare_amount
        FROM 
          `tbd-master.nyc_taxi.tripdata`
        WHERE 
          trip_distance > 1 AND trip_distance < 30 AND
          fare_amount > 1 AND 
          PULocationID IS NOT NULL AND 
          DOLocationID IS NOT NULL AND
          tpep_pickup_datetime IS NOT NULL AND
          tpep_dropoff_datetime IS NOT NULL AND
          TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, MINUTE) > 1;
    """,
    "training_testing_split": """
        CREATE OR REPLACE TABLE `tbd-master.nyc_taxi.training_data` AS
        SELECT * 
        FROM `tbd-master.nyc_taxi.filtered_tripdata`
        WHERE MOD(FARM_FINGERPRINT(CAST(trip_distance AS STRING)), 10) < 8;

        CREATE OR REPLACE TABLE `tbd-master.nyc_taxi.testing_data` AS
        SELECT * 
        FROM `tbd-master.nyc_taxi.filtered_tripdata`
        WHERE MOD(FARM_FINGERPRINT(CAST(trip_distance AS STRING)), 10) >= 8;
    """,
    "create_regr_model": """
        CREATE OR REPLACE MODEL `tbd-master.nyc_taxi.fare_prediction_model`
        OPTIONS(
          model_type='LINEAR_REG',
          input_label_cols=['fare_amount']
        ) AS
        SELECT 
          trip_distance,
          PULocationID,
          DOLocationID,
          trip_duration_minutes,
          pickup_hour,
          pickup_day_of_week,
          fare_amount
        FROM 
          `tbd-master.nyc_taxi.training_data`;
    """,
    "evaluate_model": """
        SELECT *
        FROM ML.EVALUATE(MODEL `tbd-master.nyc_taxi.fare_prediction_model`,
        (
          SELECT 
            trip_distance,
            PULocationID,
            DOLocationID,
            trip_duration_minutes,
            pickup_hour,
            pickup_day_of_week,
            fare_amount
          FROM 
            `tbd-master.nyc_taxi.testing_data`
        ));
    """
}

# Rularea query-urilor
for step, query in queries.items():
    print(f"Rulez query-ul: {step}")
    job = client.query(query)
    if step == "evaluate_model":
        # Afișează rezultatele evaluării modelului
        results = job.result()
        print("Rezultatele evaluării modelului:")
        for row in results:
            for metric, value in row.items():
                print(f"{metric}: {value}")
    else:
        # Așteaptă finalizarea job-ului
        job.result()
        print(f"Query-ul '{step}' a fost finalizat cu succes.")
