""" Config """
import os

from pydantic_settings import BaseSettings


class LogSettings(BaseSettings):
    cur_dir: str = os.path.dirname(os.path.abspath(__file__))
    parent_dir: str = os.path.dirname(cur_dir)
    project_dir: str = os.path.dirname(parent_dir)
    log_config_filename: str = f'{cur_dir}/log_conf.yaml'
    log_rotation_filename: str = f'{project_dir}/logs/logs.log'


log_settings = LogSettings()


class PGSettings(BaseSettings):
    """Settings"""

    class Config:
        """env file location"""

        env_file = log_settings.project_dir + '/.env'
        env_file_encoding = 'utf-8'

    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_port: int | None = None
    postgres_host: str | None = None


pg_settings = PGSettings()

dsn = {
    'dbname': pg_settings.postgres_db,
    'user': pg_settings.postgres_user,
    'password': pg_settings.postgres_password,
    'host': pg_settings.postgres_host,
    'port': pg_settings.postgres_port,
}

if not os.path.exists(f'{log_settings.project_dir}/logs'):
    os.makedirs(f'{log_settings.project_dir}/logs')

sqlite_file: str = f'{log_settings.project_dir}/src/db/db.sqlite'
