import sqlite3

def connect_db():
    return sqlite3.connect('customers.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            phone TEXT PRIMARY KEY,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_customer(phone):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM customers WHERE phone = ?', (phone,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_customer(phone, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO customers (phone, name) VALUES (?, ?)
        ON CONFLICT(phone) DO UPDATE SET name = excluded.name
    ''', (phone, name))
    conn.commit()
    conn.close()