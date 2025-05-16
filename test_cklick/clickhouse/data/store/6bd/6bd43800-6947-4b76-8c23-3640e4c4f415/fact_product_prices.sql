ATTACH TABLE _ UUID 'a1c12eeb-11a9-44e1-9ea2-896d71212d9c'
(
    `price_id` UInt32,
    `product_id` UInt32,
    `price` Decimal(10, 2),
    `effective_from` DateTime,
    `effective_to` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY price_id
ORDER BY price_id
SETTINGS index_granularity = 8192
