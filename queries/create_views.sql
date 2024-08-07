create or replace view sales_by_category_location_v as
select
     ordrs.order_id
     , c.customer_id
     , p.category
     , c.country
     , c.created_at
     , ordrs.total_price
     , ordrs.quantity
from orders ordrs
         left join products p on ordrs.product_id = p.product_id
         left join customers c on ordrs.customer_id = c.customer_id;
create or replace view supplier_product_count_v as
select
     ordrs.quantity
     , p.category
     , sup.seller_name
     , sup.contact_email
     , sup.product_count
     , sup.country
from suppliers sup
         left join orders ordrs on sup.product_id = ordrs.product_id
         left join products p on sup.product_id = p.product_id;
create or replace view orders_v as
select
       ordrs.product_id,
       ordrs.customer_id,
       ordrs.order_id,
       c.first_name || ' ' || c.last_name as full_name,
       c.country,
       ordrs.order_date,
       concat(cast(year (order_date) as char), lpad(cast(month (order_date) as char), 2, '0')) as monthkey,
       ordrs.quantity,
       ordrs.unit_price,
       ordrs.total_price
from customers as c
         left join orders as ordrs on c.customer_id = ordrs.customer_id;
create or replace view returns_order_v as
select
      r.order_id
     , sbl.category
     , r.return_reason
     , r.return_status
     , sbl.total_price
from returns r
         left join sales_by_category_location_v sbl on r.order_id = sbl.order_id;