CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_tripdata_with_zones` AS
SELECT 
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
  tr.airport_fee,
  
  -- Coordonatele pentru pickup location
  pu.Latitude AS pickup_latitude,
  pu.Longitude AS pickup_longitude,
  
  -- Coordonatele pentru dropoff location
  do.Latitude AS dropoff_latitude,
  do.Longitude AS dropoff_longitude

FROM 
  `tbd-24-25.nyc_taxi.tripdata` tr
LEFT JOIN 
  `tbd-24-25.nyc_taxi.taxi_zones_with_coords` pu
ON 
  tr.PULocationID = pu.LocationID  -- Join pentru pickup location

LEFT JOIN 
  `tbd-24-25.nyc_taxi.taxi_zones_with_coords` do
ON 
  tr.DOLocationID = do.LocationID;  -- Join pentru dropoff location
