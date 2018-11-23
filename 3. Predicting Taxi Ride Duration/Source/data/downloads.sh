#!/usr/bin/env bash

#Open taxi data from http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

#Taxi zone data
#wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -P ./geo_data
#wget https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip
#unzip ./taxi_zones.zip

#Yellow cab data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-07.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-08.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-09.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-10.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-11.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2017-12.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-01.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-02.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-03.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-04.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-05.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-06.csv -P ./taxi_data

#Green cab data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-07.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-08.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-09.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-10.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-11.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2017-12.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-01.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-02.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-03.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-04.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-05.csv -P ./taxi_data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2018-06.csv -P ./taxi_data

#Consolidate yellow taxi data and extract relevant info
echo "VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,PULocationID,DOLocationID,passenger_count,trip_distance,total_amount" > ./taxi_data/consolidated_yellow_tripdata.csv
ls ./taxi_data/*yellow_tripdata* | grep -v consolidated | while read f;
do
echo ${f}
grep '^[0-9]' ${f} | awk -F',' -v OFS=',' '{print $1,$2,$3,$8,$9,$4,$5,$17}' >> ./taxi_data/consolidated_yellow_tripdata.csv
done

#Consolidate green taxi data and extract relevant info
echo "VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,PULocationID,DOLocationID,passenger_count,trip_distance,total_amount" > ./taxi_data/consolidated_green_tripdata.csv
ls ./taxi_data/*green_tripdata* | grep -v consolidated | while read f;
do
echo ${f}
grep '^[0-9]' ${f} | awk -F',' -v OFS=',' '{print $1,$2,$3,$6,$7,$8,$9,$17}' >> ./taxi_data/consolidated_green_tripdata.csv
done




