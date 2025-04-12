-- Примеры SQL-запросов для розничной аналитики

-- Запрос 1: Покажи топ-10 товаров по продажам за последний месяц
SELECT p.product_name, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id WHERE s.sale_date >= date_trunc('month', CURRENT_DATE) GROUP BY p.product_name ORDER BY total_quantity DESC LIMIT 10;

-- Запрос 2: Какие магазины имеют наибольшую выручку в категории 'Молочные продукты'?
SELECT st.store_name, st.format, st.city, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON s.store_id = st.store_id WHERE c.category_name = 'Молочные продукты' GROUP BY st.store_name, st.format, st.city ORDER BY total_revenue DESC LIMIT 10;

-- Запрос 3: Сравни продажи по регионам за первый квартал этого года
SELECT st.region, SUM(s.total_amount) as total_revenue, COUNT(DISTINCT s.sale_id) as transaction_count, SUM(s.quantity) as total_quantity FROM sales s JOIN stores st ON s.store_id = st.store_id WHERE s.sale_date BETWEEN date_trunc('year', CURRENT_DATE) AND date_trunc('year', CURRENT_DATE) + INTERVAL '3 months' GROUP BY st.region ORDER BY total_revenue DESC;

-- Запрос 4: Как изменилась средняя маржа по категориям товаров за последние 3 месяца?
WITH monthly_margin AS (SELECT c.category_name, date_trunc('month', s.sale_date) as month, (SUM((s.unit_price - p.unit_cost) * s.quantity) / SUM(s.total_amount)) * 100 as margin_percentage FROM sales s JOIN products p ON s.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id WHERE s.sale_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY c.category_name, date_trunc('month', s.sale_date)) SELECT category_name, month, margin_percentage, margin_percentage - LAG(margin_percentage) OVER (PARTITION BY category_name ORDER BY month) as margin_change FROM monthly_margin ORDER BY category_name, month;

-- Запрос 5: Какие товары чаще всего покупают вместе с хлебом?
WITH bread_sales AS (SELECT sale_id FROM sales s JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name = 'Хлеб') SELECT p.product_name, COUNT(*) as purchase_frequency FROM sales s JOIN bread_sales bs ON s.sale_id = bs.sale_id JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name != 'Хлеб' GROUP BY p.product_name ORDER BY purchase_frequency DESC LIMIT 10;

-- Запрос 6: Покажи динамику продаж мороженого по месяцам за прошлый год
SELECT date_trunc('month', s.sale_date) as month, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name = 'Мороженое' AND s.sale_date BETWEEN date_trunc('year', CURRENT_DATE) - INTERVAL '1 year' AND date_trunc('year', CURRENT_DATE) - INTERVAL '1 day' GROUP BY date_trunc('month', s.sale_date) ORDER BY month;

-- Запрос 7: Какие клиенты потратили больше всего в прошлом месяце и что они покупали?
SELECT c.customer_id, c.first_name, c.last_name, SUM(s.total_amount) as total_spent, string_agg(DISTINCT p.product_name, ', ') as purchased_products FROM sales s JOIN customers c ON s.customer_id = c.customer_id JOIN products p ON s.product_id = p.product_id WHERE s.sale_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month' AND s.sale_date < date_trunc('month', CURRENT_DATE) GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_spent DESC LIMIT 10;

-- Запрос 8: Какие категории товаров приносят наибольшую прибыль в магазинах формата мини-маркет?
SELECT c.category_name, SUM((s.unit_price - p.unit_cost) * s.quantity) as total_profit, SUM(s.total_amount) as total_revenue, (SUM((s.unit_price - p.unit_cost) * s.quantity) / SUM(s.total_amount)) * 100 as margin_percentage FROM sales s JOIN products p ON s.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON s.store_id = st.store_id WHERE st.format = 'мини-маркет' GROUP BY c.category_name ORDER BY total_profit DESC;

-- Запрос 9: Сравни эффективность промо-акций за последний квартал
SELECT pr.promo_name, pr.promo_type, COUNT(DISTINCT s.sale_id) as transaction_count, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue, AVG(s.discount) * 100 as avg_discount_percentage FROM sales s JOIN promotions pr ON s.promo_id = pr.promo_id WHERE s.sale_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY pr.promo_name, pr.promo_type ORDER BY total_revenue DESC;

-- Запрос 10: У каких товаров критический уровень запасов в магазинах Москвы?
SELECT p.product_name, c.category_name, st.store_name, i.quantity as current_stock, i.min_stock_level, (i.quantity - i.min_stock_level) as stock_difference FROM inventory i JOIN products p ON i.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON i.store_id = st.store_id WHERE i.quantity < i.min_stock_level AND st.city = 'Москва' ORDER BY stock_difference ASC;

-- Запрос 11: Посчитай коэффициент эластичности для товаров
WITH prev_month AS (SELECT product_id, SUM(quantity) AS total_qty, AVG(unit_price) AS avg_price FROM sales WHERE sale_date BETWEEN DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1' MONTH) AND DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1' DAY GROUP BY product_id), curr_month AS (SELECT product_id, SUM(quantity) AS total_qty, AVG(unit_price) AS avg_price FROM sales WHERE sale_date >= DATE_TRUNC('month', CURRENT_DATE) GROUP BY product_id) SELECT c.product_id, pr.product_name, c.total_qty as 'current_qty', p.total_qty as 'new_qty', c.avg_price as 'current_price', p.avg_price as 'new_price', ROUND(((c.total_qty - p.total_qty) / p.total_qty) / ((c.avg_price - p.avg_price) / p.avg_price), 2) AS price_elasticity FROM curr_month AS c INNER JOIN prev_month AS p ON c.product_id = p.product_id INNER JOIN products AS pr ON c.product_id = pr.product_id WHERE p.total_qty > 0 AND p.avg_price > 0 AND c.avg_price <> p.avg_price ORDER BY price_elasticity DESC;

