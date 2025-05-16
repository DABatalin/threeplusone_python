ATTACH TABLE _ UUID 'b2270c00-8634-4c09-ab92-635513b407dd'
(
    `category_id` UInt32,
    `category_name` String,
    `parent_category_id` Nullable(UInt32),
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY category_id
SETTINGS index_granularity = 8192
