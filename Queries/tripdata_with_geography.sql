CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_geography` AS
SELECT
  tr.*,
  -- Crearea punctelor geografice pentru pickup și dropoff
  ST_GeogPoint(tz_pickup.Longitude, tz_pickup.Latitude) AS pickup_location,
  ST_GeogPoint(tz_dropoff.Longitude, tz_dropoff.Latitude) AS dropoff_location
FROM
  `tbd-24-25.nyc_taxi.tripdata` tr
LEFT JOIN
  `tbd-24-25.nyc_taxi.taxi_zones_with_coords` tz_pickup
  ON tr.PULocationID = tz_pickup.LocationID
LEFT JOIN
  `tbd-24-25.nyc_taxi.taxi_zones_with_coords` tz_dropoff
  ON tr.DOLocationID = tz_dropoff.LocationID;