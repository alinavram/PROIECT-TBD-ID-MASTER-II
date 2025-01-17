CREATE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_latlong` AS
SELECT
  *,
  ST_Y(pickup_location) AS pickup_latitude,
  ST_X(pickup_location) AS pickup_longitude,
  ST_Y(dropoff_location) AS dropoff_latitude,
  ST_X(dropoff_location) AS dropoff_longitude
FROM
  `tbd-24-25.nyc_taxi.taxi_tripdata_with_geography`
