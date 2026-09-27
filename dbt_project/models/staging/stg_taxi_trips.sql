select
    vendorid              as vendor_id,
    tpep_pickup_datetime  as pickup_at,
    tpep_dropoff_datetime as dropoff_at,
    passenger_count,
    trip_distance,
    fare_amount,
    total_amount,
    pulocationid          as pickup_zone_id
from {{ source('raw', 'taxi_trips') }}
where fare_amount > 0
  and trip_distance > 0