select
    ordr_v.order_id
    ,scv.category as category
     , ordr_v.quantity
     , ordr_v.total_price
    ,strftime('%Y-%m-%d', ordr_v.order_date) as order_date
from orders_v ordr_v
left join sales_by_category_location_v scv on scv.order_id = ordr_v.order_id