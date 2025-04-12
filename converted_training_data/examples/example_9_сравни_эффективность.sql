-- Запрос: Сравни эффективность промо-акций за последний квартал

SELECT pr.promo_name, pr.promo_type, COUNT(DISTINCT s.sale_id) as transaction_count, SUM(s.quantity) as total_quantity, SUM(s.total_amount) as total_revenue, AVG(s.discount) * 100 as avg_discount_percentage FROM sales s JOIN promotions pr ON s.promo_id = pr.promo_id WHERE s.sale_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY pr.promo_name, pr.promo_type ORDER BY total_revenue DESC;
