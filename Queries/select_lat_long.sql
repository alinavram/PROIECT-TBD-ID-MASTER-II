SELECT 
  LocationID, 
  borough, 
  zone, 
  ST_Y(ST_Centroid(ST_GeogFromText(the_geom))) AS Latitude, 
  ST_X(ST_Centroid(ST_GeogFromText(the_geom))) AS Longitude
FROM `tbd-24-25.nyc_taxi.taxi_zones`;
