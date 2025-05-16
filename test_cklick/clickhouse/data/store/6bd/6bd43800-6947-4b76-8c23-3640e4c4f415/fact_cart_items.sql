ATTACH TABLE _ UUID '3360b311-fd09-42f2-b270-9dce390005d3'
(
    `cart_item_id` UInt64,
    `user_id` UInt32,
    `product_id` UInt32,
    `quantity` UInt32,
    `added_at` DateTime,
    `removed_at` Nullable(DateTime),
    `purchased` Bool DEFAULT false,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY cart_item_id
ORDER BY cart_item_id
SETTINGS index_granularity = 8192
