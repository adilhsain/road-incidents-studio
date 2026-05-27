import sqlite3
import logging
from pathlib import Path

# Optional import for mysql-specific error handling (if mysql connector present)
try:
    import mysql.connector as mysql_connector
except Exception:
    mysql_connector = None

DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "road_incidents.db"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "database" / "schema.sql"
SEED_PATH = Path(__file__).resolve().parents[1] / "database" / "seed_data.sql"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_database():
    """Create and seed the local SQLite database if it is missing or uninitialized."""
    try:
        if not DATABASE_PATH.exists():
            DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(DATABASE_PATH) as conn:
                schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
                seed_sql = SEED_PATH.read_text(encoding="utf-8")
                conn.executescript(schema_sql + "\n" + seed_sql)
            logger.info("Created and seeded SQLite database at %s", DATABASE_PATH)
            return

        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            required_tables = {"PERSON", "ACCIDENT", "personas", "team_members"}
            recreate_db = False

            if not required_tables.issubset(tables):
                recreate_db = True
            else:
                cursor.execute("SELECT COUNT(*) FROM PERSON")
                person_count = cursor.fetchone()[0] or 0
                cursor.execute("SELECT COUNT(*) FROM personas")
                persona_count = cursor.fetchone()[0] or 0
                cursor.execute("SELECT COUNT(*) FROM team_members")
                team_count = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT COUNT(*) FROM ("
                    "SELECT 1 FROM personas "
                    "GROUP BY name, age, occupation, background, goals, pain_points, assigned_student, image_url "
                    "HAVING COUNT(*) > 1)"
                )
                duplicate_personas = cursor.fetchone()[0] or 0
                cursor.execute(
                    "SELECT COUNT(*) FROM ("
                    "SELECT 1 FROM team_members "
                    "GROUP BY full_name, student_number, role "
                    "HAVING COUNT(*) > 1)"
                )
                duplicate_team = cursor.fetchone()[0] or 0

                if person_count == 0 or persona_count == 0 or team_count == 0 or duplicate_personas > 0 or duplicate_team > 0:
                    recreate_db = True

        if recreate_db:
            reset_sql = (
                "DROP TABLE IF EXISTS team_members;"
                "DROP TABLE IF EXISTS personas;"
                "DROP TABLE IF EXISTS facts;"
                "DROP TABLE IF EXISTS PERSON;"
                "DROP TABLE IF EXISTS ACCIDENT;"
                "DROP TABLE IF EXISTS VEHICLE;"
                "DROP TABLE IF EXISTS NODE;"
            )
            with sqlite3.connect(DATABASE_PATH) as conn:
                schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
                seed_sql = SEED_PATH.read_text(encoding="utf-8")
                conn.executescript(reset_sql + "\n" + schema_sql + "\n" + seed_sql)
            logger.info("Recreated and seeded SQLite database at %s", DATABASE_PATH)
            return
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)


def get_db_connection():
    initialize_database()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query, params=None):
    """Execute a query and return list of dict rows.

    Returns an empty list on any database error and logs the exception.
    """
    params = params or []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        if mysql_connector is not None and isinstance(e, getattr(mysql_connector, 'Error', Exception)):
            logger.error("MySQL connector error executing query: %s", e)
        else:
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
