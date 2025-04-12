-- Запрос: Какие клиенты потратили больше всего в прошлом месяце и что они покупали?

SELECT c.customer_id, c.first_name, c.last_name, SUM(s.total_amount) as total_spent, string_agg(DISTINCT p.product_name, ', ') as purchased_products FROM sales s JOIN customers c ON s.customer_id = c.customer_id JOIN products p ON s.product_id = p.product_id WHERE s.sale_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month' AND s.sale_date < date_trunc('month', CURRENT_DATE) GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_spent DESC LIMIT 10;
