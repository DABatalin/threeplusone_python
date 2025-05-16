#!/bin/bash

# Create database
echo "CREATE DATABASE IF NOT EXISTS ecommerce" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create categories table
echo "CREATE TABLE IF NOT EXISTS ecommerce.categories (
    category_id UInt32,
    category_name String,
    parent_category_id Nullable(UInt32),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY category_id" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create sellers table
echo "CREATE TABLE IF NOT EXISTS ecommerce.sellers (
    seller_id UInt32,
    seller_name String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY seller_id" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create products table
echo "CREATE TABLE IF NOT EXISTS ecommerce.products (
    product_id UInt32,
    category_id UInt32,
    seller_id UInt32,
    product_name String,
    price Decimal(10,2),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY product_id" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create users table
echo "CREATE TABLE IF NOT EXISTS ecommerce.users (
    user_id UInt32,
    username String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create sales table
echo "CREATE TABLE IF NOT EXISTS ecommerce.sales (
    sale_id UInt32,
    product_id UInt32,
    user_id UInt32,
    seller_id UInt32,
    quantity UInt32,
    price_at_sale Decimal(10,2),
    sale_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (sale_date, sale_id)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create product ratings table
echo "CREATE TABLE IF NOT EXISTS ecommerce.product_ratings (
    rating_id UInt32,
    product_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create seller ratings table
echo "CREATE TABLE IF NOT EXISTS ecommerce.seller_ratings (
    rating_id UInt32,
    seller_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create user sessions table
echo "CREATE TABLE IF NOT EXISTS ecommerce.user_sessions (
    session_id UInt32,
    user_id UInt32,
    session_start DateTime,
    session_end DateTime,
    click_count UInt32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (session_start, session_id)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Create cart items table
echo "CREATE TABLE IF NOT EXISTS ecommerce.cart_items (
    cart_item_id UInt32,
    user_id UInt32,
    product_id UInt32,
    quantity UInt32,
    added_at DateTime,
    status Enum8('in_cart' = 1, 'purchased' = 2, 'abandoned' = 3),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (added_at, cart_item_id)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @- 