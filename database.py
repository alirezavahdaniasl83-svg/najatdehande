import os
import sqlite3
from datetime import datetime, timezone


# Railway Volume
# در Railway، Volume روی /data متصل شده است.
if os.path.isdir("/data"):
    DB_PATH = "/data/database.db"
else:
    DB_PATH = "database.db"


def get_connection():
    """Create a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Initialize the database and create the devices table.
    Compatible with the existing main.py.
    """

    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                model TEXT NOT NULL,
                android_version TEXT NOT NULL,
                battery INTEGER DEFAULT 0,
                online INTEGER DEFAULT 0,
                last_seen TEXT
            )
        """)

        conn.commit()

    finally:
        conn.close()


def init_db():
    """Alias for initialize_database."""
    initialize_database()


def register_device(
    device_id,
    name,
    model,
    android_version,
    battery=0,
    online=1
):
    """Register a device or update an existing device."""

    now = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO devices (
                device_id,
                name,
                model,
                android_version,
                battery,
                online,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(device_id) DO UPDATE SET
                name = excluded.name,
                model = excluded.model,
                android_version = excluded.android_version,
                battery = excluded.battery,
                online = excluded.online,
                last_seen = excluded.last_seen
        """, (
            device_id,
            name,
            model,
            android_version,
            battery,
            online,
            now
        ))

        conn.commit()

    finally:
        conn.close()


def get_devices():
    """Get all registered devices."""

    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT
                device_id,
                name,
                model,
                android_version,
                battery,
                online,
                last_seen
            FROM devices
            ORDER BY last_seen DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        conn.close()


def get_device(device_id):
    """Get one device by ID."""

    conn = get_connection()

    try:
        cursor = conn.execute("""
            SELECT
                device_id,
                name,
                model,
                android_version,
                battery,
                online,
                last_seen
            FROM devices
            WHERE device_id = ?
        """, (device_id,))

        row = cursor.fetchone()

        if row:
            return dict(row)

        return None

    finally:
        conn.close()


def update_device_status(
    device_id,
    online,
    battery=None
):
    """Update device online status and battery."""

    now = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    try:

        if battery is not None:

            conn.execute("""
                UPDATE devices
                SET
                    online = ?,
                    battery = ?,
                    last_seen = ?
                WHERE device_id = ?
            """, (
                online,
                battery,
                now,
                device_id
            ))

        else:

            conn.execute("""
                UPDATE devices
                SET
                    online = ?,
                    last_seen = ?
                WHERE device_id = ?
            """, (
                online,
                now,
                device_id
            ))

        conn.commit()

    finally:
        conn.close()


def delete_device(device_id):
    """Delete a device."""

    conn = get_connection()

    try:

        conn.execute("""
            DELETE FROM devices
            WHERE device_id = ?
        """, (device_id,))

        conn.commit()

    finally:
        conn.close()


# Initialize database on startup
initialize_database()
