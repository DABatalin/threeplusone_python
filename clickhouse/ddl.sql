CREATE DATABASE IF NOT EXISTS ecommerce;

USE ecommerce;

CREATE TABLE IF NOT EXISTS categories (
    category_id UInt32,
    category_name String,
    parent_category_id Nullable(UInt32),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY category_id;


CREATE TABLE IF NOT EXISTS sellers (
    seller_id UInt32,
    seller_name String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY seller_id;

CREATE TABLE IF NOT EXISTS products (
    product_id UInt32,
    category_id UInt32,
    seller_id UInt32,
    product_name String,
    price Decimal(10,2),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY product_id;

CREATE TABLE IF NOT EXISTS users (
    user_id UInt32,
    username String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id;

CREATE TABLE IF NOT EXISTS sales (
    sale_id UInt32,
    product_id UInt32,
    user_id UInt32,
    seller_id UInt32,
    quantity UInt32,
    price_at_sale Decimal(10,2),
    sale_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (sale_date, sale_id);

CREATE TABLE IF NOT EXISTS product_ratings (
    rating_id UInt32,
    product_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id);

CREATE TABLE IF NOT EXISTS seller_ratings (
    rating_id UInt32,
    seller_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id);

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id UInt32,
    user_id UInt32,
    session_start DateTime,
    session_end DateTime,
    click_count UInt32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (session_start, session_id);

CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id UInt32,
    user_id UInt32,
    product_id UInt32,
    quantity UInt32,
    added_at DateTime,
    status Enum8('in_cart' = 1, 'purchased' = 2, 'abandoned' = 3),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (added_at, cart_item_id);


CREATE TABLE IF NOT EXISTS daily_sales_aggregation (
    date Date,
    total_sales UInt32,
    total_quantity UInt32,
    total_revenue Decimal(15,2),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY date;

CREATE TABLE IF NOT EXISTS user_activity_aggregation (
    user_id UInt32,
    total_sessions UInt32,
    total_clicks UInt32,
    avg_clicks_per_session Float32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id; 