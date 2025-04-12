-- Запрос: Покажи топ-10 товаров по продажам за последний месяц

SELECT p.product_name, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id WHERE s.sale_date >= date_trunc('month', CURRENT_DATE) GROUP BY p.product_name ORDER BY total_quantity DESC LIMIT 10;
