CREATE OR REPLACE TABLE `tbd-24-25.nyc_taxi.taxi_zones_with_coords` AS
SELECT 
  LocationID, 
  borough, 
  zone, 
  ST_Y(ST_Centroid(ST_GeogFromText(the_geom))) AS Latitude, 
  ST_X(ST_Centroid(ST_GeogFromText(the_geom))) AS Longitude,
  ST_GeogPoint(ST_X(ST_Centroid(ST_GeogFromText(the_geom))), ST_Y(ST_Centroid(ST_GeogFromText(the_geom)))) AS Location
FROM `tbd-24-25.nyc_taxi.taxi_zones`;