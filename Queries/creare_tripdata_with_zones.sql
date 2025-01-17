CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.tripdata_with_zones` AS
SELECT 
  t.*,
  pu.Latitude AS Pickup_Latitude,
  pu.Longitude AS Pickup_Longitude,
  do.Latitude AS Dropoff_Latitude,
  do.Longitude AS Dropoff_Longitude
FROM `tbd-24-25.nyc_taxi.tripdata` t
LEFT JOIN `tbd-24-25.nyc_taxi.taxi_zones_with_coords` pu
  ON t.PULocationID = pu.LocationID
LEFT JOIN `tbd-24-25.nyc_taxi.taxi_zones_with_coords` do
  ON t.DOLocationID = do.LocationID;
