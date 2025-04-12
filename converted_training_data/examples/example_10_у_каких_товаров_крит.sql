-- Запрос: У каких товаров критический уровень запасов в магазинах Москвы?

SELECT p.product_name, c.category_name, st.store_name, i.quantity as current_stock, i.min_stock_level, (i.quantity - i.min_stock_level) as stock_difference FROM inventory i JOIN products p ON i.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id JOIN stores st ON i.store_id = st.store_id WHERE i.quantity < i.min_stock_level AND st.city = 'Москва' ORDER BY stock_difference ASC;
