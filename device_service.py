from datetime import datetime, timezone

from database import get_connection


def register_device(
    device_id: str,
    name: str | None = None,
    model: str | None = None,
    android_version: str | None = None,
    battery: int | None = None,
):
    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    connection.execute(
        """
        INSERT INTO devices (
            device_id,
            name,
            model,
            android_version,
            battery,
            online,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?, 1, ?)
        ON CONFLICT(device_id) DO UPDATE SET
            name = excluded.name,
            model = excluded.model,
            android_version = excluded.android_version,
            battery = excluded.battery,
            online = 1,
            last_seen = excluded.last_seen
        """,
        (
            device_id,
            name,
            model,
            android_version,
            battery,
            now,
        ),
    )

    connection.commit()
    connection.close()


def get_devices():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            device_id,
            name,
            model,
            android_version,
            battery,
            online,
            last_seen
        FROM devices
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
