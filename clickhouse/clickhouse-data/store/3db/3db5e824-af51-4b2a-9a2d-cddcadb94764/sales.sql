ATTACH TABLE _ UUID '665c0196-a6d7-4965-a16c-c1dc343a5bcc'
(
    `sale_id` UInt32,
    `product_id` UInt32,
    `user_id` UInt32,
    `seller_id` UInt32,
    `quantity` UInt32,
    `price_at_sale` Decimal(10, 2),
    `sale_date` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (sale_date, sale_id)
SETTINGS index_granularity = 8192
