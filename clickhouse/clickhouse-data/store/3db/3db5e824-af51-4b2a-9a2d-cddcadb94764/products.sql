ATTACH TABLE _ UUID '3b43a5f9-36c8-4919-a9fe-9cf060bae96f'
(
    `product_id` UInt32,
    `category_id` UInt32,
    `seller_id` UInt32,
    `product_name` String,
    `price` Decimal(10, 2),
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY product_id
SETTINGS index_granularity = 8192
