""" CRUD for PostgresSQL """
from typing import Any
from uuid import UUID

from fastapi import APIRouter

from src.core.logger import logger
from src.schemas.schemas_tables import UsersTable
from src.service.postgres import RepositoryPG

router = APIRouter(tags=['CRUD for POSTGRESQL'], prefix='/postgres')


@router.post('/get_row_number_by_table')
async def get_row_number_by_table(params: UsersTable) -> Any:
    """Get row number by table"""
    return RepositoryPG(params=params).get_row_number_by_table()


@router.post('/get_all_table_names')
async def get_all_table_names(params: UsersTable) -> Any:
    """Get all table names"""
    postgres_db = RepositoryPG(params)
    return postgres_db.get_all_table_names()


@router.post('/get_all_records')
async def get_all_records(params: UsersTable) -> Any:
    """Get all records"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.get_all_records()


@router.post('/get_by_id')
async def get_by_id(item_id: UUID, params: UsersTable) -> Any:
    """Get by id"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.get_by_id(item_id=item_id)


@router.post('/create_table')
async def create_table(params: UsersTable) -> dict:
    """Create table"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.create_table()


@router.post('/insert_one')
async def insert_one(
    params: UsersTable,
    item_id: str | None = None,
    name: str | None = None,
) -> Any:
    """Insert one"""
    logger.info(f'POST item_id: {item_id}, name: {name}')
    postgres_db = RepositoryPG(params=params)
    result = postgres_db.insert_one(item_id=item_id, name=name)
    return result


@router.post('/insert_many')
async def insert_many(
    params: UsersTable,
    names: list[str],
) -> Any:
    """Insert many"""
    postgres_db = RepositoryPG(params=params)
    result = postgres_db.insert_many(names)
    return result


@router.post('/truncate_table')
async def truncate_table(params: UsersTable) -> dict:
    """Truncate table"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.truncate_table()


@router.post('/truncate_all_tables')
async def truncate_all_tables(params: UsersTable) -> dict:
    """Truncate all tables"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.truncate_all_tables()


@router.post('/drop_table')
async def drop_table(params: UsersTable) -> dict:
    """Drop table"""
    postgres_db = RepositoryPG(params=params)
    return postgres_db.drop_table()
