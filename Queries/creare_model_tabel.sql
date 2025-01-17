CREATE OR REPLACE MODEL `tbd-24-25.nyc_taxi.taxi_fare_model`
OPTIONS(
    model_type='linear_reg',
    input_label_cols=['total_amount']
) AS
SELECT 
    trip_distance, 
    passenger_count, 
    payment_type, 
    PULocationID, 
    DOLocationID, 
    total_amount
FROM `tbd-master.nyc_taxi.tripdata`
WHERE total_amount > 0;
