ATTACH TABLE _ UUID 'f8bda4e7-af24-413b-8bf8-60d84b21a97f'
(
    `product_id` UInt32,
    `category_id` UInt32,
    `seller_id` UInt32,
    `product_name` String,
    `price` Decimal(10, 2),
    `rating` Float32,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY product_id
ORDER BY product_id
SETTINGS index_granularity = 8192
