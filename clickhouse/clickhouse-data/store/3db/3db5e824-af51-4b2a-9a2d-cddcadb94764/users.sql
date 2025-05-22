ATTACH TABLE _ UUID '903323f2-5945-4418-86bd-2a423cecae69'
(
    `user_id` UInt32,
    `username` String,
    `registration_date` Date,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY user_id
SETTINGS index_granularity = 8192
