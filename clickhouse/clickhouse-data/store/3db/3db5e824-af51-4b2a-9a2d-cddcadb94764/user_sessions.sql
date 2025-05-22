ATTACH TABLE _ UUID '2cb83904-5608-4812-8483-76ead607d158'
(
    `session_id` UInt32,
    `user_id` UInt32,
    `session_start` DateTime,
    `session_end` DateTime,
    `click_count` UInt32,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (session_start, session_id)
SETTINGS index_granularity = 8192
