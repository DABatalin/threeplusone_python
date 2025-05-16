ATTACH TABLE _ UUID '87da8957-3a65-49c9-8c8c-f49240eca3c6'
(
    `seller_id` UInt32,
    `seller_name` String,
    `registration_date` Date,
    `rating` Float32,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY seller_id
ORDER BY seller_id
SETTINGS index_granularity = 8192
