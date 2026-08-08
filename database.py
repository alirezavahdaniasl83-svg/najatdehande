import os
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "database.db")
)


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            name TEXT,
            model TEXT,
            android_version TEXT,
            battery INTEGER,
            online INTEGER DEFAULT 0,
            last_seen TEXT
        )
    """)

    connection.commit()
    connection.close()
