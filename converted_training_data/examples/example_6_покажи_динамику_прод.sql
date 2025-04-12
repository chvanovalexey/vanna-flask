-- Запрос: Покажи динамику продаж мороженого по месяцам за прошлый год

SELECT date_trunc('month', s.sale_date) as month, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name = 'Мороженое' AND s.sale_date BETWEEN date_trunc('year', CURRENT_DATE) - INTERVAL '1 year' AND date_trunc('year', CURRENT_DATE) - INTERVAL '1 day' GROUP BY date_trunc('month', s.sale_date) ORDER BY month;
