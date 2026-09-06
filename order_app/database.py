import sqlite3


class OrderDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
    def create_connection(self):
        conn= sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys= ON;")
        return conn
    
    def create_tables(self):
        with self.create_connection() as conn:
            c = conn.cursor()  
            
            c.execute("""
                    CREATE TABLE IF NOT EXISTS customers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE)
                        """)
            c.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                    )""")
    def save_customer(self, name):
        with self.create_connection() as conn:
            c = conn.cursor()
            c.execute("""
                    INSERT OR IGNORE INTO customers(name)
                    VALUES(?)
                    """, (name,))
            customer_id = c.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchone()
            return customer_id[0]
    def save_order(self, customer_id, product_name, quantity, unit_price, total):
        with self.create_connection() as conn:
            c = conn.cursor()
            c.execute("""
                    INSERT INTO orders(
                    customer_id, product_name, quantity, unit_price, total)
                    VALUES(?, ?, ?, ?, ?)
                    """,(customer_id, product_name, quantity, unit_price, total))

    def get_orders(self):
        with self.create_connection() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""SELECT name, product_name, quantity, unit_price, total
                FROM orders
                INNER JOIN customers
                ON orders.customer_id = customers.id
                """)
            rows = c.fetchall()
        return [dict(row) for row in rows]

