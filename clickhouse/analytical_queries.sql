SELECT 
    c.category_name,
    count() as sales_count,
    sum(s.quantity) as total_items_sold,
    round(sum(s.price_at_sale * s.quantity), 2) as total_revenue
FROM ecommerce.sales s
JOIN ecommerce.products p ON s.product_id = p.product_id
JOIN ecommerce.categories c ON p.category_id = c.category_id
WHERE s.sale_date >= now() - INTERVAL 30 DAY
GROUP BY c.category_name
ORDER BY total_revenue DESC;

SELECT 
    s.seller_id,
    sel.seller_name,
    count(DISTINCT s.sale_id) as orders_count,
    sum(s.quantity) as items_sold,
    round(sum(s.price_at_sale * s.quantity), 2) as total_revenue,
    round(avg(sr.rating), 2) as avg_rating
FROM ecommerce.sales s
JOIN ecommerce.sellers sel ON s.seller_id = sel.seller_id
LEFT JOIN ecommerce.seller_ratings sr ON sel.seller_id = sr.seller_id
GROUP BY s.seller_id, sel.seller_name
ORDER BY total_revenue DESC
LIMIT 10;

SELECT 
    status,
    count() as count,
    round(count() * 100.0 / sum(count()) OVER (), 2) as percentage
FROM ecommerce.cart_items
GROUP BY status
ORDER BY count DESC;

SELECT 
    toDayOfWeek(session_start) as day_of_week,
    count() as sessions_count,
    round(avg(dateDiff('minute', session_start, session_end)), 2) as avg_session_duration_minutes,
    round(avg(click_count), 2) as avg_clicks_per_session
FROM ecommerce.user_sessions
GROUP BY day_of_week
ORDER BY day_of_week;

SELECT 
    c.category_name,
    count(pr.rating_id) as total_ratings,
    round(avg(pr.rating), 2) as avg_rating,
    bar(avg(pr.rating), 0, 5, 20) as rating_distribution
FROM ecommerce.products p
JOIN ecommerce.categories c ON p.category_id = c.category_id
LEFT JOIN ecommerce.product_ratings pr ON p.product_id = pr.product_id
GROUP BY c.category_name
ORDER BY avg_rating DESC;

SELECT 
    toDate(sale_date) as date,
    count(DISTINCT sale_id) as orders_count,
    count(DISTINCT user_id) as unique_customers,
    sum(quantity) as items_sold,
    round(sum(price_at_sale * quantity), 2) as daily_revenue
FROM ecommerce.sales
WHERE sale_date >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date;

WITH user_orders AS (
    SELECT 
        user_id,
        count(DISTINCT sale_id) as orders_count
    FROM ecommerce.sales
    GROUP BY user_id
)
SELECT 
    orders_count as purchases_made,
    count() as users_count,
    round(count() * 100.0 / sum(count()) OVER (), 2) as percentage
FROM user_orders
GROUP BY orders_count
ORDER BY orders_count;

WITH product_views AS (
    SELECT 
        p.category_id,
        us.click_count
    FROM ecommerce.user_sessions us
    JOIN ecommerce.products p ON us.user_id = us.user_id -- предполагаем, что клики связаны с просмотром товаров
)
SELECT 
    c.category_name,
    sum(pv.click_count) as total_views,
    round(sum(pv.click_count) * 100.0 / sum(sum(pv.click_count)) OVER (), 2) as percentage
FROM product_views pv
JOIN ecommerce.categories c ON pv.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_views DESC;

SELECT 
    time_to_purchase_days,
    count() as users_count
FROM (
    SELECT 
        u.user_id,
        min(dateDiff('day', u.registration_date, toDate(s.sale_date))) as time_to_purchase_days
    FROM ecommerce.users u
    JOIN ecommerce.sales s ON u.user_id = s.user_id
    GROUP BY u.user_id
)
GROUP BY time_to_purchase_days
ORDER BY time_to_purchase_days; 