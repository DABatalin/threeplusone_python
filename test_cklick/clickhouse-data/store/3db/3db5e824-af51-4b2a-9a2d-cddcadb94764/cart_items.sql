ATTACH TABLE _ UUID '2580b42e-176c-4bce-950d-786db2aeaf7f'
(
    `cart_item_id` UInt32,
    `user_id` UInt32,
    `product_id` UInt32,
    `quantity` UInt32,
    `added_at` DateTime,
    `status` Enum8('in_cart' = 1, 'purchased' = 2, 'abandoned' = 3),
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (added_at, cart_item_id)
SETTINGS index_granularity = 8192
