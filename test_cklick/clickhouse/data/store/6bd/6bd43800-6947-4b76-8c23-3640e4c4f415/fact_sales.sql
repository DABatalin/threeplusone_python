ATTACH TABLE _ UUID '68a5936e-8268-4669-9763-01149f932843'
(
    `sale_id` UInt32,
    `product_id` UInt32,
    `user_id` UInt32,
    `seller_id` UInt32,
    `quantity` UInt32,
    `sale_price` Decimal(10, 2),
    `sale_date` DateTime,
    `created_at` DateTime DEFAULT now()
)
ENGINE = MergeTree
PRIMARY KEY sale_id
ORDER BY sale_id
SETTINGS index_granularity = 8192
