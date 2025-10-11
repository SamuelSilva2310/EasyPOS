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