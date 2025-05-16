#!/bin/bash

# Insert categories
echo "INSERT INTO ecommerce.categories (category_id, category_name, parent_category_id) VALUES
(1, 'Electronics', NULL),
(2, 'Smartphones', 1),
(3, 'Laptops', 1),
(4, 'Clothing', NULL),
(5, 'Men''s Wear', 4),
(6, 'Women''s Wear', 4)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert sellers
echo "INSERT INTO ecommerce.sellers (seller_id, seller_name, registration_date) VALUES
(1, 'TechHub Store', '2023-01-01'),
(2, 'Fashion World', '2023-02-15'),
(3, 'Gadget Galaxy', '2023-03-20'),
(4, 'Style Studio', '2023-04-10'),
(5, 'Digital Dreams', '2023-05-05')" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert products
echo "INSERT INTO ecommerce.products (product_id, category_id, seller_id, product_name, price) VALUES
(1, 2, 1, 'iPhone 14 Pro', 999.99),
(2, 2, 3, 'Samsung Galaxy S23', 899.99),
(3, 3, 1, 'MacBook Pro M2', 1499.99),
(4, 3, 3, 'Dell XPS 13', 1299.99),
(5, 5, 2, 'Classic Denim Jeans', 79.99),
(6, 5, 4, 'Cotton T-Shirt', 29.99),
(7, 6, 2, 'Summer Dress', 89.99),
(8, 6, 4, 'Elegant Blouse', 59.99)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert users
echo "INSERT INTO ecommerce.users (user_id, username, registration_date) VALUES
(1, 'john_doe', '2023-01-15'),
(2, 'jane_smith', '2023-02-20'),
(3, 'mike_wilson', '2023-03-25'),
(4, 'sarah_brown', '2023-04-30'),
(5, 'david_clark', '2023-05-10')" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert sales
echo "INSERT INTO ecommerce.sales (sale_id, product_id, user_id, seller_id, quantity, price_at_sale, sale_date) VALUES
(1, 1, 1, 1, 1, 999.99, '2024-01-15 10:30:00'),
(2, 2, 2, 3, 1, 899.99, '2024-01-20 14:45:00'),
(3, 5, 3, 2, 2, 79.99, '2024-02-01 16:20:00'),
(4, 7, 4, 2, 1, 89.99, '2024-02-10 11:15:00'),
(5, 3, 5, 1, 1, 1499.99, '2024-02-15 09:30:00')" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert product ratings
echo "INSERT INTO ecommerce.product_ratings (rating_id, product_id, user_id, rating, rating_date) VALUES
(1, 1, 1, 5, '2024-01-20 15:30:00'),
(2, 2, 2, 4, '2024-01-25 16:45:00'),
(3, 5, 3, 5, '2024-02-05 12:20:00'),
(4, 7, 4, 4, '2024-02-15 14:15:00'),
(5, 3, 5, 5, '2024-02-20 10:30:00')" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert seller ratings
echo "INSERT INTO ecommerce.seller_ratings (rating_id, seller_id, user_id, rating, rating_date) VALUES
(1, 1, 1, 5, '2024-01-20 15:35:00'),
(2, 3, 2, 4, '2024-01-25 16:50:00'),
(3, 2, 3, 5, '2024-02-05 12:25:00'),
(4, 2, 4, 4, '2024-02-15 14:20:00'),
(5, 1, 5, 5, '2024-02-20 10:35:00')" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert user sessions
echo "INSERT INTO ecommerce.user_sessions (session_id, user_id, session_start, session_end, click_count) VALUES
(1, 1, '2024-01-15 10:00:00', '2024-01-15 10:45:00', 15),
(2, 2, '2024-01-20 14:30:00', '2024-01-20 15:00:00', 12),
(3, 3, '2024-02-01 16:00:00', '2024-02-01 16:30:00', 8),
(4, 4, '2024-02-10 11:00:00', '2024-02-10 11:30:00', 10),
(5, 5, '2024-02-15 09:15:00', '2024-02-15 09:45:00', 20)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @-

# Insert cart items
echo "INSERT INTO ecommerce.cart_items (cart_item_id, user_id, product_id, quantity, added_at, status) VALUES
(1, 1, 1, 1, '2024-01-15 10:15:00', 2),
(2, 2, 2, 1, '2024-01-20 14:35:00', 2),
(3, 3, 5, 2, '2024-02-01 16:10:00', 2),
(4, 4, 7, 1, '2024-02-10 11:05:00', 2),
(5, 5, 3, 1, '2024-02-15 09:20:00', 2),
(6, 1, 4, 1, '2024-02-20 13:30:00', 1),
(7, 2, 6, 2, '2024-02-21 15:45:00', 3),
(8, 3, 8, 1, '2024-02-22 11:20:00', 1)" | curl 'http://localhost:8123/?user=default&password=clickhouse' --data-binary @- 