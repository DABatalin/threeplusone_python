-- Create database
CREATE DATABASE IF NOT EXISTS ecommerce;

-- Use the database
USE ecommerce;

-- Categories dimension
CREATE TABLE IF NOT EXISTS categories (
    category_id UInt32,
    category_name String,
    parent_category_id Nullable(UInt32),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY category_id;

-- Sellers dimension
CREATE TABLE IF NOT EXISTS sellers (
    seller_id UInt32,
    seller_name String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY seller_id;

-- Products dimension
CREATE TABLE IF NOT EXISTS products (
    product_id UInt32,
    category_id UInt32,
    seller_id UInt32,
    product_name String,
    price Decimal(10,2),
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY product_id;

-- Users dimension
CREATE TABLE IF NOT EXISTS users (
    user_id UInt32,
    username String,
    registration_date Date,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY user_id;

-- Sales fact table
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

-- Product ratings fact table
CREATE TABLE IF NOT EXISTS product_ratings (
    rating_id UInt32,
    product_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id);

-- Seller ratings fact table
CREATE TABLE IF NOT EXISTS seller_ratings (
    rating_id UInt32,
    seller_id UInt32,
    user_id UInt32,
    rating UInt8,
    rating_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (rating_date, rating_id);

-- User sessions fact table
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id UInt32,
    user_id UInt32,
    session_start DateTime,
    session_end DateTime,
    click_count UInt32,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (session_start, session_id);

-- Cart items fact table
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