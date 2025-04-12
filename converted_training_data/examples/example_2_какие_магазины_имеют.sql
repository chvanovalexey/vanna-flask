-- Запрос: Какие магазины имеют наибольшую выручку в категории 'Молочные продукты'?

SELECT st.store_name, st.format, st.city, SUM(s.total_amount) as total_revenue FROM sales s JOIN products p ON s.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON s.store_id = st.store_id WHERE c.category_name = 'Молочные продукты' GROUP BY st.store_name, st.format, st.city ORDER BY total_revenue DESC LIMIT 10;
