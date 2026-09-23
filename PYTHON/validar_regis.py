import sqlite3

conn = sqlite3.connect("manufacturing.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM production_orders"
)

print(cursor.fetchone())

conn.close()