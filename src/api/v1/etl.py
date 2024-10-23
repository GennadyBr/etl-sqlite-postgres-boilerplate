from typing import Any

from fastapi import APIRouter

from src.service.etl import etl_all

router = APIRouter(tags=['ETL'], prefix='/etl')


@router.get('/sqlite-to-postgres')
async def etl() -> Any:
    """ETL"""
    return etl_all()
