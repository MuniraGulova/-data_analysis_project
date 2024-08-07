create table products
(
    product_id   integer primary key,
    product_name text,
    category     varchar(150),
    price        float,
    stock_status varchar(100)
);
create table customers
(
    customer_id integer primary key,
    first_name  varchar(100),
    last_name   varchar(100),
    email       varchar(100),
    phone       varchar(50),
    country     varchar(100),
    address     varchar(100),
    created_at  timestamp
);
create table orders
(
    order_id    integer primary key,
    product_id  integer,
    customer_id integer,
    order_date  timestamp,
    status      varchar(100),
    quantity    integer,
    unit_price  float,
    total_price float,
    foreign key ("product_id") references products ("product_id"),
    foreign key ("customer_id") references customers ("customer_id")
);
create table payment_info
(
    payment_id   integer primary key,
    order_id     integer,
    name_on_card varchar(100),
    card_number  text,
    card_expire  varchar(100),
    cvv_number   integer,
    foreign key ("order_id") references orders ("order_id")
);
create table returns
(
    order_id      integer,
    customer_id   integer,
    return_reason varchar(100),
    return_status varchar(100),
    foreign key ("order_id") references orders ("order_id"),
    foreign key ("customer_id") references customers ("customer_id")
);
create table suppliers
(
    seller_id     integer primary key,
    product_id    integer,
    seller_name   varchar(100),
    contact_name  varchar(100),
    contact_email varchar(100),
    contact_phone varchar(50),
    country       varchar(100),
    product_count float,
    foreign key ("product_id") references products ("product_id")
);