from src.core.logger import logger
from src.schemas.schemas_tables import UserTables
from src.service.postgres import RepositoryPG
from src.service.sqlite import RepositorySQLite


def _get_sqlite_info(table_name: str, transfer_report: dict) -> dict:
    transfer_report[table_name] = {
        'sqlite_row_count': RepositorySQLite.get_row_number_by_table(
            table_name,
        ),
    }
    return transfer_report


def _step(sqlite_row_qty: int, step: int, i: int) -> int:
    return step if i + step < sqlite_row_qty else sqlite_row_qty - i


def _get_pg_info(params: UserTables, transfer_report: dict) -> dict:
    transfer_report[params.table_name]['pg_row_count'] = RepositoryPG(
        params,
    ).get_row_number_by_table()[0]
    return transfer_report


def etl_all() -> dict:
    step = 1000
    transfer_report: dict = {}
    for table_name in RepositorySQLite.get_all_table_names():
        params = UserTables(schema_name='content', table_name=table_name)
        transfer_report = _get_sqlite_info(table_name, transfer_report)
        transfer_report = _get_pg_info(params, transfer_report)
        transfer_report[table_name]['loaded_count'] = 0
        logger.info(f'{table_name=}: {transfer_report=}')
        for i in range(
            0,
            transfer_report[table_name]['sqlite_row_count'],
            step,
        ):
            offset = i
            limit = _step(
                transfer_report[table_name]['sqlite_row_count'],
                step,
                i,
            )
            data = RepositorySQLite.get_all_records(table_name, limit, offset)

            pg = RepositoryPG(params)
            ids: list = pg.insert_by_table_name(data)

            transfer_report[table_name]['loaded_count'] += len(ids)

    return transfer_report
