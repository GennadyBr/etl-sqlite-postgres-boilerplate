import requests
from fastapi import APIRouter

from src.core.logger import logger

router = APIRouter()


@router.get('/hello')
async def hello() -> dict:
    """Hello world"""
    logger.info('Hello World')
    return {'message': 'Hello World'}


@router.get('/request')
async def request() -> str:
    """Request example"""
    response = requests.get('https://google.com')
    result = f'Google Response: {response.status_code}'
    logger.info(result)
    return result


@router.get('/raise_error')
async def raise_error() -> str:
    """Raise Error"""
    try:
        div_zero = 1 / 0
    except ZeroDivisionError as error:
        logger.exception('Divide by zero error')
        return str(error)
    return str(div_zero)
