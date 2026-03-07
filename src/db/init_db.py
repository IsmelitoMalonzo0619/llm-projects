from .connection import get_connection

def create_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            city TEXT PRIMARY KEY,
            price REAL
        )
        """)
        conn.commit()

ticket_prices = {"london": 799, "paris": 899, "tokyo": 1420, "sydney": 2999}

def insert_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        for city, price in ticket_prices.items():
            cursor.execute("""
                INSERT INTO prices (city, price) 
                VALUES (?, ?)
                ON CONFLICT(city) DO UPDATE SET price=excluded.price
            """, (city.lower(), price))
        conn.commit()

def initialize_db():
    create_db()
    insert_db()
