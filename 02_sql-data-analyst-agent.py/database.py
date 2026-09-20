import sqlite3
import os
import pandas as pd

DB_PATH = "data/sales.db"

os.makedirs("data", exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            age INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, name, city, age)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Arun", "Chennai", 25),
        (2, "Priya", "Coimbatore", 29),
        (3, "Karthik", "Salem", 31),
        (4, "Divya", "Chennai", 27),
        (5, "Rahul", "Madurai", 35),
        (6, "Meena", "Trichy", 24),
        (7, "Vijay", "Chennai", 32),
        (8, "Anitha", "Coimbatore", 28),
    ])

    cursor.executemany("""
        INSERT OR IGNORE INTO products
        (product_id, product_name, category, price)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Laptop", "Electronics", 75000),
        (2, "Phone", "Electronics", 30000),
        (3, "Headphones", "Electronics", 5000),
        (4, "Keyboard", "Accessories", 2500),
        (5, "Mouse", "Accessories", 1500),
        (6, "Monitor", "Electronics", 18000),
        (7, "Backpack", "Accessories", 3000),
        (8, "Tablet", "Electronics", 25000),
    ])

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, product_id, quantity, order_date)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 1, 1, 1, "2026-01-10"),
        (2, 2, 2, 2, "2026-01-12"),
        (3, 3, 3, 3, "2026-01-15"),
        (4, 4, 1, 1, "2026-02-01"),
        (5, 5, 4, 4, "2026-02-05"),
        (6, 6, 5, 5, "2026-02-10"),
        (7, 7, 2, 1, "2026-02-15"),
        (8, 8, 6, 2, "2026-02-20"),
        (9, 1, 8, 1, "2026-03-01"),
        (10, 2, 1, 1, "2026-03-05"),
        (11, 3, 7, 3, "2026-03-10"),
        (12, 4, 3, 2, "2026-03-15"),
        (13, 5, 2, 2, "2026-03-20"),
        (14, 6, 6, 1, "2026-03-25"),
        (15, 7, 1, 2, "2026-04-01"),
    ])

    connection.commit()
    connection.close()

def get_schema():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()
    schema = []

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema.append(f"\nTABLE: {table_name}")
        for column in columns:
            column_name = column[1]
            data_type = column[2]
            schema.append(f"  - {column_name} ({data_type})")

    connection.close()
    return "\n".join(schema)

def execute_sql(query):
    connection = get_connection()
    try:
        dataframe = pd.read_sql_query(query, connection)
        return dataframe, None
    except Exception as error:
        return None, str(error)
    finally:
        connection.close()