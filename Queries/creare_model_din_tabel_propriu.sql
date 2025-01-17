CREATE OR REPLACE MODEL `tbd-24-25.nyc_taxi.taxi_fare_model`
OPTIONS(
    model_type='linear_reg',
    input_label_cols=['total_amount']
) AS
SELECT 
    total_amount,  -- Add total_amount column here
    trip_distance, 
    passenger_count, 
    payment_type, 
    PULocationID, 
    DOLocationID, 
    fare_amount,
    congestion_surcharge,
    tip_amount,
    TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, SECOND) AS trip_duration
FROM `tbd-24-25.nyc_taxi.tripdata`
WHERE total_amount > 0;

