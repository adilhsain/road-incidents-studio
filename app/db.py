import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "road_incidents.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    params = params or []
    conn = get_db_connection()
    try:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
