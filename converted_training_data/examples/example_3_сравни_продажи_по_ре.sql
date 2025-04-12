-- Запрос: Сравни продажи по регионам за первый квартал этого года

SELECT st.region, SUM(s.total_amount) as total_revenue, COUNT(DISTINCT s.sale_id) as transaction_count, SUM(s.quantity) as total_quantity FROM sales s JOIN stores st ON s.store_id = st.store_id WHERE s.sale_date BETWEEN date_trunc('year', CURRENT_DATE) AND date_trunc('year', CURRENT_DATE) + INTERVAL '3 months' GROUP BY st.region ORDER BY total_revenue DESC;
