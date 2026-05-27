import logging
import sqlite3
from pathlib import Path

try:
    from mysql.connector import Error as MySQLError
except ImportError:
    MySQLError = Exception

DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "road_incidents.db"

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    params = params or []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except MySQLError as error:
        logging.error("Database query failed: %s", error)
        return []
    except sqlite3.Error as error:
        logging.error("SQLite query failed: %s", error)
        return []
    finally:
        if conn:
            conn.close()

def test_connection():
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        return True
    except (MySQLError, sqlite3.Error) as error:
        logging.error("Database connection test failed: %s", error)
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()
