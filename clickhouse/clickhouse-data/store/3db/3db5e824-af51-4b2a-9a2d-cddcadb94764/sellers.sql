ATTACH TABLE _ UUID 'e7b964c2-d57e-4fa7-9164-b1e8e8cfacd4'
(
    `seller_id` UInt32,
    `seller_name` String,
    `registration_date` Date,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY seller_id
SETTINGS index_granularity = 8192
