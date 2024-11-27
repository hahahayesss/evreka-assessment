import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "user": os.getenv("DB_USER", "local"),
    "password": os.getenv("DB_PASSWORD", "secret"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "location_db")
}

_INSERT_QUERY = """
INSERT INTO locations (device_id, latitude, longitude, speed, timestamp)
VALUES (%s, %s, %s, %s, %s)
"""

_FIND_LOCATIONS_BY_RANGE_QUERY = """
SELECT * FROM locations
WHERE device_id = %s AND timestamp BETWEEN %s AND %s
ORDER BY timestamp ASC
"""

_FIND_LOCATIONS_BY_LATEST = """
SELECT * FROM locations
WHERE device_id = %s
ORDER BY timestamp DESC
LIMIT 1
"""


def _get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert(device_id, latitude, longitude, speed, timestamp):
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute(_INSERT_QUERY, (device_id, latitude, longitude, speed, timestamp))
    conn.commit()
    cursor.close()
    conn.close()


def find_by_range(device_id, start_date, end_date):
    conn = _get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(_FIND_LOCATIONS_BY_RANGE_QUERY, (device_id, start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def find_by_latest(device_id):
    conn = _get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(_FIND_LOCATIONS_BY_LATEST, (device_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data
