ATTACH TABLE _ UUID 'cce29a7e-376f-4832-8fe0-851240883b32'
(
    `rating_id` UInt32,
    `seller_id` UInt32,
    `user_id` UInt32,
    `rating` UInt8,
    `rating_date` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (rating_date, rating_id)
SETTINGS index_granularity = 8192
