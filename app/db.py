import sqlite3
import logging
from pathlib import Path

# Optional import for mysql-specific error handling (if mysql connector present)
try:
    import mysql.connector as mysql_connector
except Exception:
    mysql_connector = None

DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "road_incidents.db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query, params=None):
    """Execute a query and return list of dict rows.

    Returns an empty list on any database error and logs the exception.
    """
    params = params or []
    conn = None
    # Run with explicit mysql.connector.Error handling if the module is available
    if mysql_connector is not None and hasattr(mysql_connector, 'Error'):
        try:
            conn = get_db_connection()
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except getattr(mysql_connector, 'Error') as me:
            logger.error("MySQL connector error executing query: %s", me)
            return []
        except Exception as e:
            logger.error("Database error executing query: %s", e)
            return []
    else:
        try:
            conn = get_db_connection()
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error("Database error executing query: %s", e)
            return []
    finally:
        if conn:
            conn.close()


def test_connection():
    """Simple DB connectivity test. Returns True if DB can be opened."""
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        logger.warning("Database connection test failed: %s", e)
        return False
