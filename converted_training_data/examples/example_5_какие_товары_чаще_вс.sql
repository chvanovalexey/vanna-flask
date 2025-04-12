-- Запрос: Какие товары чаще всего покупают вместе с хлебом?

WITH bread_sales AS (SELECT sale_id FROM sales s JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name = 'Хлеб') SELECT p.product_name, COUNT(*) as purchase_frequency FROM sales s JOIN bread_sales bs ON s.sale_id = bs.sale_id JOIN products p ON s.product_id = p.product_id JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id WHERE sc.subcategory_name != 'Хлеб' GROUP BY p.product_name ORDER BY purchase_frequency DESC LIMIT 10;
