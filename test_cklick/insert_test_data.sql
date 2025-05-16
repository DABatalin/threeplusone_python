-- Insert categories (3 уровня категорий)
INSERT INTO ecommerce.categories (category_id, category_name, parent_category_id) VALUES
(1, 'Электроника', NULL),
(2, 'Одежда', NULL),
(3, 'Дом и сад', NULL),
(4, 'Смартфоны', 1),
(5, 'Ноутбуки', 1),
(6, 'Аудиотехника', 1),
(7, 'Мужская одежда', 2),
(8, 'Женская одежда', 2),
(9, 'Детская одежда', 2),
(10, 'Садовый инвентарь', 3),
(11, 'Мебель', 3),
(12, 'Освещение', 3),
(13, 'iPhone', 4),
(14, 'Samsung', 4),
(15, 'Xiaomi', 4),
(16, 'Gaming', 5),
(17, 'Business', 5),
(18, 'Наушники', 6),
(19, 'Колонки', 6),
(20, 'Микрофоны', 6);

-- Insert sellers (100 продавцов)
INSERT INTO ecommerce.sellers (seller_id, seller_name, registration_date)
WITH
(
    SELECT arrayJoin(range(1, 101)) AS id,
    concat('Seller_', toString(id)) AS name,
    toDate('2023-01-01') - toIntervalDay(rand() % 365) AS reg_date
)
SELECT id, name, reg_date;

-- Insert products (1000 товаров)
INSERT INTO ecommerce.products (product_id, category_id, seller_id, product_name, price)
WITH
(
    SELECT 
        arrayJoin(range(1, 1001)) AS id,
        (rand() % 20) + 1 AS cat_id,
        (rand() % 100) + 1 AS s_id,
        concat('Product_', toString(id)) AS name,
        round(rand() % 100000 + 1000, 2) / 100 AS product_price
)
SELECT id, cat_id, s_id, name, product_price;

-- Insert users (10000 пользователей)
INSERT INTO ecommerce.users (user_id, username, registration_date)
WITH
(
    SELECT 
        arrayJoin(range(1, 10001)) AS id,
        concat('User_', toString(id)) AS name,
        toDate('2023-01-01') - toIntervalDay(rand() % 730) AS reg_date
)
SELECT id, name, reg_date;

-- Insert sales (100000 продаж за последний год)
INSERT INTO ecommerce.sales (sale_id, product_id, user_id, seller_id, quantity, price_at_sale, sale_date)
WITH
(
    SELECT 
        arrayJoin(range(1, 100001)) AS id,
        (rand() % 1000) + 1 AS p_id,
        (rand() % 10000) + 1 AS u_id,
        (rand() % 100) + 1 AS s_id,
        (rand() % 5) + 1 AS qty,
        round(rand() % 100000 + 1000, 2) / 100 AS sale_price,
        now() - toIntervalDay(rand() % 365) - toIntervalSecond(rand() % 86400) AS s_date
)
SELECT id, p_id, u_id, s_id, qty, sale_price, s_date;

-- Insert product ratings (50000 оценок)
INSERT INTO ecommerce.product_ratings (rating_id, product_id, user_id, rating, rating_date)
WITH
(
    SELECT 
        arrayJoin(range(1, 50001)) AS id,
        (rand() % 1000) + 1 AS p_id,
        (rand() % 10000) + 1 AS u_id,
        (rand() % 5) + 1 AS r,
        now() - toIntervalDay(rand() % 365) - toIntervalSecond(rand() % 86400) AS r_date
)
SELECT id, p_id, u_id, r, r_date;

-- Insert seller ratings (25000 оценок)
INSERT INTO ecommerce.seller_ratings (rating_id, seller_id, user_id, rating, rating_date)
WITH
(
    SELECT 
        arrayJoin(range(1, 25001)) AS id,
        (rand() % 100) + 1 AS s_id,
        (rand() % 10000) + 1 AS u_id,
        (rand() % 5) + 1 AS r,
        now() - toIntervalDay(rand() % 365) - toIntervalSecond(rand() % 86400) AS r_date
)
SELECT id, s_id, u_id, r, r_date;

-- Insert user sessions (200000 сессий)
INSERT INTO ecommerce.user_sessions (session_id, user_id, session_start, session_end, click_count)
WITH
(
    SELECT 
        arrayJoin(range(1, 200001)) AS id,
        (rand() % 10000) + 1 AS u_id,
        now() - toIntervalDay(rand() % 365) - toIntervalSecond(rand() % 86400) AS start_time,
        now() - toIntervalDay(rand() % 365) - toIntervalSecond(rand() % 43200) AS end_time,
        (rand() % 100) + 1 AS clicks
)
SELECT id, u_id, start_time, if(start_time > end_time, start_time + toIntervalMinute(rand() % 120), end_time), clicks;

-- Insert cart items (30000 товаров в корзинах)
INSERT INTO ecommerce.cart_items (cart_item_id, user_id, product_id, quantity, added_at, status)
WITH
(
    SELECT 
        arrayJoin(range(1, 30001)) AS id,
        (rand() % 10000) + 1 AS u_id,
        (rand() % 1000) + 1 AS p_id,
        (rand() % 5) + 1 AS qty,
        now() - toIntervalDay(rand() % 30) - toIntervalSecond(rand() % 86400) AS add_date,
        ['in_cart', 'purchased', 'abandoned'][rand() % 3 + 1] AS st
)
SELECT id, u_id, p_id, qty, add_date, st; 