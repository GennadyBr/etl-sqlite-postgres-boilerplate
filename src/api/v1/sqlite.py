""" CRUD for SQLite """
from typing import Any

from fastapi import APIRouter

from src.service.sqlite import RepositorySQLite

router = APIRouter(tags=['CRUD for SQLite'], prefix='/sqlite')


@router.get('/get_all_table_names')
async def get_all_table_names() -> Any:
    """Get all table names"""
    sqlite = RepositorySQLite()
    result = sqlite.get_all_table_names()
    return result


@router.get('/get_batch_records')
async def get_all_records(
    table_name: str = 'film_work', limit: int = 10, offset: int = 0,
) -> Any:
    """Get all records"""
    sqlite = RepositorySQLite()
    result = sqlite.get_all_records(table_name, limit, offset)
    return result


@router.get('/get_row_number_by_table')
async def get_row_number_by_table(table_name: str = 'film_work') -> Any:
    """Get row number by table"""
    sqlite = RepositorySQLite()
    result = sqlite.get_row_number_by_table(table_name)
    return result
