import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

# Database path - can be overridden
DATABASE_PATH = "data.db"


class DatabaseConnection:
    """Manages SQLite database connections"""

    _database_path = DATABASE_PATH

    @classmethod
    def set_database_path(cls, path: str) -> None:
        """Set custom database path"""
        cls._database_path = path
        global DATABASE_PATH
        DATABASE_PATH = path

    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator[sqlite3.Connection, None, None]:
        """
        Get a database connection using context manager.
        Ensures connections are properly closed.
        """
        connection = sqlite3.connect(cls._database_path)
        try:
            yield connection
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(f"Database error: {e}") from e
        finally:
            connection.close()

    @classmethod
    def execute_query(
        cls, query: str, params: tuple = None, fetch_one: bool = False
    ):
        """
        Execute a query and optionally fetch results.
        Handles connection lifecycle automatically.
        """
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())

            if fetch_one:
                return cursor.fetchone()
            elif "SELECT" in query.upper():
                return cursor.fetchall()

            return None


# Module-level functions for convenience
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection - module-level convenience function"""
    return DatabaseConnection.get_connection()
