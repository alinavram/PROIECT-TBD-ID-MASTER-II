CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_boroughs` AS
SELECT
  *,
  DATE(tpep_pickup_datetime) AS pickup_date,
  DATE(tpep_dropoff_datetime) AS dropoff_date
FROM
  `tbd-24-25.nyc_taxi.taxi_tripdata_with_boroughs`
