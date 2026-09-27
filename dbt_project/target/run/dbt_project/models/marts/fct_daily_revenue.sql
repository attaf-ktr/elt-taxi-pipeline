
  
    

create or replace transient table TAXI_DB.ANALYTICS.fct_daily_revenue
    
    
    
    
    

    as (select
    date_trunc('day', pickup_at) as trip_date,
    pickup_zone_id,
    count(*)                     as trip_count,
    sum(total_amount)            as total_revenue,
    avg(trip_distance)           as avg_distance
from TAXI_DB.ANALYTICS.stg_taxi_trips
group by 1, 2
    )
;


  