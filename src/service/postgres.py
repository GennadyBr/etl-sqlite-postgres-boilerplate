""" Service for PostgresSQL """
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import names
from psycopg import Cursor

from src.core.error_messages import ErrorMessages
from src.db.db import PGReturn, pg_execute
from src.schemas.postgres import (FilmWork, Genre, GenreFilmWork, Person,
                                  PersonFilmWork, PGExecuteData)
from src.schemas.schemas_tables import UsersTable
from src.schemas.users import Users


class RepositoryPG:
    """Repository PostgresSQL class"""

    def __init__(self, params: UsersTable):
        self.params: UsersTable = params

    @staticmethod
    def _name(name: str | None) -> str | None:
        """Name"""
        if name is None:
            return None
        return name.replace("'", "`")

    @staticmethod
    def _date(date: datetime | None) -> datetime:
        if date is None:
            return datetime.now()
        return date

    @staticmethod
    def _rating(rating: float | None) -> float:
        if rating is None:
            return 0
        return rating

    def get_all_records(self) -> PGReturn:
        """Get all records"""
        params = PGExecuteData(
            query=f'SELECT * FROM '
            f'{self.params.schema_name}.{self.params.table_name};',
        )
        return pg_execute(params)

    def get_by_id(self, item_id: UUID) -> PGReturn:
        """Get by id"""
        params = PGExecuteData(
            query=f"SELECT * FROM "
            f"{self.params.schema_name}.{self.params.table_name} "
            f"WHERE id = '{item_id}';",
            multi=False,
        )
        result = pg_execute(params)

        if not result:
            return {'message': 'Item not found'}
        return result

    def get_all_table_names(self) -> Any:
        """Get all table names"""
        params = PGExecuteData(
            query=f"SELECT table_name "
            f"FROM information_schema.tables "
            f"WHERE table_schema = '{self.params.schema_name}';",
        )
        return pg_execute(params)

    def create_schema(self) -> None:
        """Create schema"""
        params = PGExecuteData(
            query=f'CREATE SCHEMA IF NOT EXISTS {self.params.schema_name};',
            is_result=False,
        )
        pg_execute(params)

    def ping_db(self) -> bool:
        """Ping db"""
        params = PGExecuteData(
            query=f'SELECT 1 FROM '
            f'{self.params.schema_name}.{self.params.table_name};',
            is_result=True,
        )
        result = pg_execute(params)
        if isinstance(result, Cursor | list):
            return True
        if result is None or isinstance(result, ErrorMessages):
            return False
        return False

    def create_table(self) -> dict:
        """Create table"""
        self.create_schema()

        if self.ping_db():
            return {'message': 'Table already exists'}

        params = PGExecuteData(
            query=(
                f'CREATE TABLE IF NOT EXISTS '
                f'{self.params.schema_name}.{self.params.table_name} '
                f'(id uuid PRIMARY KEY, name text);'
            ),
            is_result=False,
        )
        pg_execute(params)
        return {'message': 'Table created'}

    def truncate_table(self) -> dict:
        """Truncate table"""
        if self.ping_db():
            params = PGExecuteData(
                query=f'TRUNCATE TABLE '
                f'{self.params.schema_name}.{self.params.table_name} '
                f'CASCADE;',
                is_result=False,
            )
            pg_execute(params)
            return {'message': 'Table truncated'}
        return {'message': 'Table NOT exist'}

    def truncate_all_tables(self) -> dict:
        """Truncate all tables"""
        table_names: list = self.get_all_table_names()
        truncated_tables: list = []
        for row in table_names:
            table_name: str = row[0]
            self.params.table_name = table_name
            self.truncate_table()
            truncated_tables.append(table_name)

        return {'message': f'All tables {truncated_tables} truncated'}

    def drop_table(self) -> dict:
        """Drop table"""
        if not self.ping_db():
            return {'message': 'Table NOT exist'}

        params = PGExecuteData(
            query=f'DROP TABLE IF EXISTS '
            f'{self.params.schema_name}.{self.params.table_name} '
            f'CASCADE;',
            is_result=False,
        )
        pg_execute(params)
        return {'message': 'Table dropped'}

    def insert_one(
        self, item_id: str | None = None, name: str | None = None,
    ) -> PGReturn:
        """Insert one"""
        if item_id is None:
            item_id = str(uuid4())
        if name is None:
            name = names.get_full_name()
        insert_params = PGExecuteData(
            query=(
                f"INSERT INTO {self.params.schema_name}."
                f"{self.params.table_name} "
                f"(id, name) "
                f"VALUES ('{item_id}', '{name}') "
                f"ON CONFLICT (id) DO UPDATE SET name = excluded.name "
                f"RETURNING id;"
            ),
            multi=False,
            is_result=True,
        )

        return pg_execute(insert_params)

    def insert_many(self, item_names: list[str]) -> PGReturn:
        """Insert many"""
        users: list[Users] = [
            Users(id=uuid4(), name=item_name) for item_name in item_names
        ]
        data = ', '.join(f"('{user.id}', '{user.name}')" for user in users)

        insert_params = PGExecuteData(
            query=f'INSERT '
            f'INTO {self.params.schema_name}.{self.params.table_name} '
            f'(id, name) VALUES {data} '
            f'ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name '
            f'RETURNING id;',
            multi=True,
            is_result=True,
        )

        return pg_execute(insert_params)

    def insert_by_table_name(self, data: list[dict]) -> Any:
        """Insert by table name"""

        params = PGExecuteData(
            query=self._insert_query(data),
            multi=True,
            is_result=True,
        )
        ids = pg_execute(params)
        return ids

    def get_row_number_by_table(self) -> Any:
        """Get row number by table"""
        params = PGExecuteData(
            query=f"SELECT COUNT(*) FROM {self.params.schema_name}."
            f"{self.params.table_name};",
            multi=False,
            is_result=True,
        )
        result = pg_execute(params)
        return result

    def _data(self, data: list) -> dict:
        """Data"""
        result: dict = {}
        match self.params.table_name:
            case 'genre':
                genre_data: list[Genre] = [Genre(**row) for row in data]
                result['data'] = ', '.join(
                    f"('{genre.id}', '{self._name(genre.name)}', "
                    f"'{self._name(genre.description)}', "
                    f"'{genre.created_at}', '{genre.updated_at}')"
                    for genre in genre_data
                )
                result[
                    'fields'
                ] = '(id, name, description, created_at, updated_at) '
            case 'person':
                person_data: list[Person] = [Person(**row) for row in data]
                result['data'] = ', '.join(
                    f"""('{person.id}', '{self._name(person.full_name)}',
                    '{person.created_at}', '{person.updated_at}')"""
                    for person in person_data
                )
                result['fields'] = '(id, full_name, created_at, updated_at) '
            case 'film_work':
                film_work_data: list[FilmWork] = [
                    FilmWork(**row) for row in data
                ]
                result['data'] = ', '.join(
                    f"('{film_work.id}', '{self._name(film_work.title)}', "
                    f"'{self._name(film_work.description)}', "
                    f"'{self._date(film_work.creation_date)}', "
                    f"'{film_work.file_path}', "
                    f"'{self._rating(film_work.rating)}', "
                    f"'{film_work.type}', '{film_work.created_at}', "
                    f"'{film_work.updated_at}')"
                    for film_work in film_work_data
                )
                result['fields'] = (
                    '(id, title, description, '
                    'creation_date, file_path, rating, '
                    'type, created_at, updated_at) '
                )
            case 'genre_film_work':
                genre_film_work_data: list[GenreFilmWork] = [
                    GenreFilmWork(**row) for row in data
                ]
                result['data'] = ', '.join(
                    f"('{genre_film_work.id}', '{genre_film_work.genre_id}', "
                    f"'{genre_film_work.film_work_id}', "
                    f"'{genre_film_work.created_at}')"
                    for genre_film_work in genre_film_work_data
                )
                result['fields'] = '(id, genre_id, film_work_id, created_at) '
            case 'person_film_work':
                person_film_work_data: list[PersonFilmWork] = [
                    PersonFilmWork(**row) for row in data
                ]
                result['data'] = ', '.join(
                    f"('{person_film_work.id}', "
                    f"'{person_film_work.film_work_id}', "
                    f"'{person_film_work.person_id}', "
                    f"'{self._name(person_film_work.role)}', "
                    f"'{person_film_work.created_at}')"
                    for person_film_work in person_film_work_data
                )
                result[
                    'fields'
                ] = '(id, film_work_id, person_id, role, created_at) '
        return result

    def _insert_query(self, data: list) -> str:
        """Insert query"""
        datas: dict = self._data(data)
        insert_query = (
            f'INSERT INTO {self.params.schema_name}.'
            f'{self.params.table_name} '
            f'{datas["fields"]}'
            f'VALUES {datas["data"]} ON CONFLICT DO NOTHING RETURNING id;'
        )

        return insert_query
