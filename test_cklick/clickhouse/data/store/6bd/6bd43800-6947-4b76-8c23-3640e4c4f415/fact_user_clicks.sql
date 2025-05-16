ATTACH TABLE _ UUID 'fc333c2a-0ad9-4550-a8d0-4e5b9f0c7df1'
(
    `click_id` UInt64,
    `user_id` UInt32,
    `product_id` UInt32,
    `session_id` String,
    `click_timestamp` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY click_id
ORDER BY click_id
SETTINGS index_granularity = 8192
