CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_boroughs` AS
SELECT
  *,
  ST_MAKELINE(pickup_location, dropoff_location) AS trip_line
FROM
  `tbd-24-25.nyc_taxi.taxi_tripdata_with_boroughs`
