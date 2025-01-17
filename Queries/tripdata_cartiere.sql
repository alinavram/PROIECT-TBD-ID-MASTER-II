CREATE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_boroughs` AS
SELECT
  t.*,
  z_pickup.Borough AS pickup_borough,
  z_pickup.Zone AS pickup_zone,
  z_dropoff.Borough AS dropoff_borough,
  z_dropoff.Zone AS dropoff_zone
FROM
  `tbd-24-25.nyc_taxi.taxi_tripdata_with_latlong` AS t
LEFT JOIN
  `tbd-24-25.nyc_taxi.taxi_zones` AS z_pickup
  ON t.PULocationID = z_pickup.LocationID
LEFT JOIN
  `tbd-24-25.nyc_taxi.taxi_zones` AS z_dropoff
  ON t.DOLocationID = z_dropoff.LocationID
