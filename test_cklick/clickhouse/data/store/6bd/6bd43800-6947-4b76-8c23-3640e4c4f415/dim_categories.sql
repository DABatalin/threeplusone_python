ATTACH TABLE _ UUID 'de40c22e-2b9c-4c1c-ae86-375e9221d10d'
(
    `category_id` UInt32,
    `category_name` String,
    `parent_category_id` Nullable(UInt32),
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY category_id
ORDER BY category_id
SETTINGS index_granularity = 8192
