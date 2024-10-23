""" Service for SQLite """
from typing import Any

from src.db.db import sqlite_execute


class RepositorySQLite:
    """Repository SQLite class"""

    @staticmethod
    def get_all_records(
        table_name: str = 'film_work', limit: int = 1000, offset: int = 0,
    ) -> list[dict]:
        """Get all records"""
        query = f'SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset};'
        result = sqlite_execute(query)
        result = [dict(row) for row in result]
        return result

    @staticmethod
    def get_all_table_names() -> Any:
        """Get all table names"""
        query = 'SELECT name FROM sqlite_master WHERE type = "table";'
        result = sqlite_execute(query)
        result = [dict(row)['name'] for row in result]
        result.sort(key=len)
        return result

    @staticmethod
    def get_row_number_by_table(table_name: str = 'film_work') -> Any:
        """Get row number by table"""
        query = f'SELECT COUNT(*) FROM {table_name};'
        result = sqlite_execute(query)
        result = [dict(row)['COUNT(*)'] for row in result]
        return result[0]
