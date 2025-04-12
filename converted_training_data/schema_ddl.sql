-- DDL для базы данных розничной торговли

-- Информация о магазинах
CREATE TABLE stores (
    store_id INTEGER -- Уникальный идентификатор магазина,
    store_name TEXT -- Название магазина,
    format TEXT -- Формат магазина,
    region TEXT -- Регион расположения,
    city TEXT -- Город,
    open_date DATE -- Дата открытия,
    size_sqm FLOAT -- Площадь магазина в квадратных метрах,
    is_active BOOLEAN -- Активен ли магазин
);

-- Информация о товарах
CREATE TABLE products (
    product_id INTEGER -- Уникальный идентификатор товара,
    product_name TEXT -- Наименование товара,
    category_id INTEGER -- Идентификатор категории,
    subcategory_id INTEGER -- Идентификатор подкатегории,
    brand TEXT -- Бренд,
    supplier_id INTEGER -- Идентификатор поставщика,
    unit_price FLOAT -- Базовая цена за единицу,
    unit_cost FLOAT -- Себестоимость единицы,
    unit_type TEXT -- Единица измерения (кг, шт, л),
    is_private_label BOOLEAN -- Является ли собственной торговой маркой
);

-- Категории товаров
CREATE TABLE categories (
    category_id INTEGER -- Уникальный идентификатор категории,
    category_name TEXT -- Название категории,
    department TEXT -- Отдел
);

-- Подкатегории товаров
CREATE TABLE subcategories (
    subcategory_id INTEGER -- Уникальный идентификатор подкатегории,
    category_id INTEGER -- Идентификатор родительской категории,
    subcategory_name TEXT -- Название подкатегории
);

-- Данные о продажах
CREATE TABLE sales (
    sale_id INTEGER -- Уникальный идентификатор продажи,
    store_id INTEGER -- Идентификатор магазина,
    product_id INTEGER -- Идентификатор товара,
    customer_id INTEGER -- Идентификатор клиента (может быть NULL),
    sale_date DATE -- Дата продажи,
    quantity FLOAT -- Количество проданных единиц,
    unit_price FLOAT -- Фактическая цена продажи за единицу,
    discount FLOAT -- Размер скидки,
    total_amount FLOAT -- Итоговая сумма продажи,
    payment_type TEXT -- Тип оплаты (наличные, карта, онлайн),
    promo_id INTEGER -- Идентификатор промо-акции (может быть NULL)
);

-- Информация о клиентах
CREATE TABLE customers (
    customer_id INTEGER -- Уникальный идентификатор клиента,
    first_name TEXT -- Имя,
    last_name TEXT -- Фамилия,
    email TEXT -- Электронная почта,
    phone TEXT -- Телефон,
    registration_date DATE -- Дата регистрации,
    loyalty_level TEXT -- Уровень лояльности,
    city TEXT -- Город,
    birth_date DATE -- Дата рождения,
    gender TEXT -- Пол
);

-- Информация о поставщиках
CREATE TABLE suppliers (
    supplier_id INTEGER -- Уникальный идентификатор поставщика,
    supplier_name TEXT -- Название поставщика,
    contact_person TEXT -- Контактное лицо,
    email TEXT -- Электронная почта,
    phone TEXT -- Телефон,
    country TEXT -- Страна,
    rating FLOAT -- Рейтинг поставщика
);

-- Информация о запасах
CREATE TABLE inventory (
    inventory_id INTEGER -- Уникальный идентификатор записи инвентаря,
    store_id INTEGER -- Идентификатор магазина,
    product_id INTEGER -- Идентификатор товара,
    quantity FLOAT -- Количество на складе,
    last_update TIMESTAMP -- Время последнего обновления,
    min_stock_level FLOAT -- Минимальный уровень запаса,
    max_stock_level FLOAT -- Максимальный уровень запаса
);

-- Информация о промо-акциях
CREATE TABLE promotions (
    promo_id INTEGER -- Уникальный идентификатор акции,
    promo_name TEXT -- Название акции,
    start_date DATE -- Дата начала,
    end_date DATE -- Дата окончания,
    promo_type TEXT -- Тип акции (скидка, 2+1, и т.д.),
    discount_amount FLOAT -- Размер скидки,
    min_purchase FLOAT -- Минимальная сумма покупки
);

-- Определения внешних ключей

-- Отношение типа many-to-one
ALTER TABLE sales ADD CONSTRAINT fk_sales_store_id_stores 
    FOREIGN KEY (store_id) REFERENCES stores(store_id);

-- Отношение типа many-to-one
ALTER TABLE sales ADD CONSTRAINT fk_sales_product_id_products 
    FOREIGN KEY (product_id) REFERENCES products(product_id);

-- Отношение типа many-to-one
ALTER TABLE sales ADD CONSTRAINT fk_sales_customer_id_customers 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Отношение типа many-to-one
ALTER TABLE sales ADD CONSTRAINT fk_sales_promo_id_promotions 
    FOREIGN KEY (promo_id) REFERENCES promotions(promo_id);

-- Отношение типа many-to-one
ALTER TABLE products ADD CONSTRAINT fk_products_category_id_categories 
    FOREIGN KEY (category_id) REFERENCES categories(category_id);

-- Отношение типа many-to-one
ALTER TABLE products ADD CONSTRAINT fk_products_subcategory_id_subcategories 
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id);

-- Отношение типа many-to-one
ALTER TABLE products ADD CONSTRAINT fk_products_supplier_id_suppliers 
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);

-- Отношение типа many-to-one
ALTER TABLE subcategories ADD CONSTRAINT fk_subcategories_category_id_categories 
    FOREIGN KEY (category_id) REFERENCES categories(category_id);

-- Отношение типа many-to-one
ALTER TABLE inventory ADD CONSTRAINT fk_inventory_store_id_stores 
    FOREIGN KEY (store_id) REFERENCES stores(store_id);

-- Отношение типа many-to-one
ALTER TABLE inventory ADD CONSTRAINT fk_inventory_product_id_products 
    FOREIGN KEY (product_id) REFERENCES products(product_id);

