ATTACH TABLE _ UUID '33349162-8b6d-43df-a272-736b4901f0e6'
(
    `user_id` UInt32,
    `username` String,
    `registration_date` Date,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY user_id
ORDER BY user_id
SETTINGS index_granularity = 8192
