import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS devices(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT UNIQUE,
    name TEXT,
    model TEXT,
    android TEXT,
    battery INTEGER,
    online INTEGER,
    last_seen TEXT
)
""")

conn.commit()
