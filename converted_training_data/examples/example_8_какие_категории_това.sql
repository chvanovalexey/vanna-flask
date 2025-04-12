-- Запрос: Какие категории товаров приносят наибольшую прибыль в магазинах формата мини-маркет?

SELECT c.category_name, SUM((s.unit_price - p.unit_cost) * s.quantity) as total_profit, SUM(s.total_amount) as total_revenue, (SUM((s.unit_price - p.unit_cost) * s.quantity) / SUM(s.total_amount)) * 100 as margin_percentage FROM sales s JOIN products p ON s.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON s.store_id = st.store_id WHERE st.format = 'мини-маркет' GROUP BY c.category_name ORDER BY total_profit DESC;
