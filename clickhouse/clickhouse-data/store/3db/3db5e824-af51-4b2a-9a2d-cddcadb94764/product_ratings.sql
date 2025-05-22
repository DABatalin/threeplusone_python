ATTACH TABLE _ UUID 'cf0e8dc9-7e3b-488e-8e1c-69808e3d00ec'
(
    `rating_id` UInt32,
    `product_id` UInt32,
    `user_id` UInt32,
    `rating` UInt8,
    `rating_date` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (rating_date, rating_id)
SETTINGS index_granularity = 8192
