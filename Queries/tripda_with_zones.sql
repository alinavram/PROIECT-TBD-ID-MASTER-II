CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_zones` AS
SELECT 
  t.LocationID,
  t.borough,
  t.zone,
  t.Latitude AS zone_latitude,
  t.Longitude AS zone_longitude,
  t.Location AS zone_location,
  tr.tpep_pickup_datetime,
  tr.tpep_dropoff_datetime,
  tr.PULocationID,
  tr.DOLocationID,
  tr.passenger_count,
  tr.trip_distance,
  tr.fare_amount,
  tr.extra,
  tr.mta_tax,
  tr.tip_amount,
  tr.tolls_amount,
  tr.improvement_surcharge,
  tr.total_amount,
  tr.congestion_surcharge,
  tr.airport_fee
FROM 
  `tbd-24-25.nyc_taxi.taxi_zones_with_coords` t
JOIN 
  `tbd-24-25.nyc_taxi.tripdata` tr
ON 
  t.LocationID = tr.PULocationID  -- Join pentru pickup location
  OR t.LocationID = tr.DOLocationID;  -- Join pentru dropoff location
