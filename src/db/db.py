"""DB"""
import sqlite3
from typing import Any, List, Union

import psycopg
from psycopg.connection import Cursor, Connection
from psycopg.rows import Row

from src.core.config import dsn, sqlite_file
from src.core.error_messages import ErrorMessages
from src.core.logger import logger
from src.schemas.postgres import PGExecuteData

PGReturn = Union[Row, ErrorMessages, str, list[Any], dict, None]


def _log_data(params: PGExecuteData) -> None:
    """Log data"""
    logger.info(f'query: {params.query}')
    logger.info(f'multi: {params.multi}')
    logger.info(f'is_result: {params.is_result}')
    logger.info(f'data: {params.data}')


def _cur_execute(
    params: PGExecuteData, cur: Cursor, conn: Connection
) -> PGReturn:
    """Execute"""
    if params.data:
        cur.executemany(params.query, params.data)
    else:
        cur.execute(params.query)

    conn.commit()

    if params.is_result and params.multi:
        return cur.fetchall()
    elif params.is_result and not params.multi:
        return cur.fetchone()
    else:
        return None


def _try_execute(
    params: PGExecuteData, cur: Cursor, conn: Connection
) -> PGReturn:
    """Try execute"""
    try:
        result = _cur_execute(params, cur, conn)

    except psycopg.errors.UndefinedTable:
        _log_data(params)
        logger.exception(ErrorMessages.TableDoesNotExist)
        result = ErrorMessages.TableDoesNotExist

    except psycopg.errors.InvalidTextRepresentation:
        _log_data(params)
        logger.exception(ErrorMessages.IDNotValid)
        result = ErrorMessages.IDNotValid

    except psycopg.OperationalError:
        _log_data(params)
        logger.exception(ErrorMessages.OperationalError)
        result = ErrorMessages.OperationalError

    except TypeError:
        _log_data(params)
        logger.exception(ErrorMessages.TypError)
        result = ErrorMessages.TypError

    except psycopg.ProgrammingError:
        _log_data(params)
        logger.exception(ErrorMessages.ProgrammingError)
        result = ErrorMessages.ProgrammingError

    except psycopg.errors.UniqueViolation:
        _log_data(params)
        logger.exception(ErrorMessages.UniqueViolation)
        result = ErrorMessages.UniqueViolation

    except psycopg.errors.ForeignKeyViolation:
        _log_data(params)
        logger.exception(ErrorMessages.ForeignKeyViolation)
        result = ErrorMessages.ForeignKeyViolation

    except AttributeError:
        _log_data(params)
        logger.exception(ErrorMessages.AttribError)
        result = ErrorMessages.AttribError

    except psycopg.errors.InvalidDatetimeFormat:
        _log_data(params)
        logger.exception(ErrorMessages.InvalidDatetimeFormat)
        result = ErrorMessages.InvalidDatetimeFormat

    except ConnectionError:
        _log_data(params)
        logger.exception(ErrorMessages.ConError)
        result = ErrorMessages.ConError

    return result


def pg_execute(
    params: PGExecuteData,
) -> PGReturn:
    """DB execute"""

    with psycopg.connect(**dsn) as conn, conn.cursor() as cur: # type: ignore
        result: PGReturn = _try_execute(params, cur, conn)
        return result


def sqlite_execute(query: str) -> Any:
    """Get connection"""
    with sqlite3.connect(sqlite_file) as conn:

        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute(query)
        result = curs.fetchall()

    return result
