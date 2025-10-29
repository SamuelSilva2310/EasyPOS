-- schema.sql
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    label TEXT NOT NULL,
    icon TEXT NOT NULL,    
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_price REAL NOT NULL,
    fully_printed BOOLEAN NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    icon TEXT, 
    category_id int,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp,
    FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE IF NOT EXISTS sales_items (
    sale_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    item_price REAL NOT NULL,
    total_price REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp,
    PRIMARY KEY (sale_id, item_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    sale_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    icon TEXT NOT NULL,
    description TEXT NOT NULL,
    printed BOOLEAN NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp,
    FOREIGN KEY (item_id) REFERENCES items (id)
);



CREATE TABLE IF NOT EXISTS schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Overview of total sales
CREATE VIEW IF NOT EXISTS view_sales_summary AS
SELECT
    COUNT(DISTINCT s.id) AS total_sales,
    SUM(s.total_price) AS total_revenue
FROM sales s;

-- Total sales per day
CREATE VIEW IF NOT EXISTS view_total_sales_per_day AS
SELECT
    DATE(s.created_at) AS sale_date,
    COUNT(s.id) AS num_sales,
    SUM(s.total_price) AS total_revenue
FROM sales s
GROUP BY DATE(s.created_at)
ORDER BY sale_date DESC;

-- Total quantity sold per item
CREATE VIEW IF NOT EXISTS view_item_sales AS
SELECT
    i.id AS item_id,
    i.name AS item_name,
    i.category_id,
    SUM(si.quantity) AS total_quantity_sold,
    SUM(si.total_price) AS total_sales_amount
FROM items i
JOIN sales_items si ON i.id = si.item_id
GROUP BY i.id, i.name, i.category_id
ORDER BY total_quantity_sold DESC;

-- Total sales per category
CREATE VIEW IF NOT EXISTS view_category_sales AS
SELECT
    c.id AS category_id,
    c.label AS category_name,
    COUNT(DISTINCT si.sale_id) AS num_sales,
    SUM(si.quantity) AS total_items_sold,
    SUM(si.total_price) AS total_revenue
FROM categories c
JOIN items i ON i.category_id = c.id
JOIN sales_items si ON si.item_id = i.id
GROUP BY c.id, c.label
ORDER BY total_revenue DESC;

-- Top selling items (quantity and revenue)
CREATE VIEW IF NOT EXISTS view_top_selling_items AS
SELECT
    i.id AS item_id,
    i.name AS item_name,
    SUM(si.quantity) AS total_quantity_sold,
    SUM(si.total_price) AS total_revenue
FROM items i
JOIN sales_items si ON si.item_id = i.id
GROUP BY i.id, i.name
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- Sales and tickets summary
CREATE VIEW IF NOT EXISTS view_sales_tickets_summary AS
SELECT
    s.id AS sale_id,
    COUNT(DISTINCT t.id) AS tickets_count,
    SUM(t.printed) AS tickets_printed,
    s.total_price AS sale_total
FROM sales s
LEFT JOIN tickets t ON t.sale_id = s.id
GROUP BY s.id
ORDER BY s.created_at DESC;