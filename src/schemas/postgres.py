from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from src.core.logger import logger


class CustomBaseModel(BaseModel):
    """Custom BaseModel"""

    class Config:
        """Custom Config"""

        from_attributes = True


class UUIDMixin(CustomBaseModel):
    """UUIDMixin"""

    id: UUID = Field(default=uuid4())


def validate_date(value: datetime | str) -> datetime | str:
    """Validate date"""
    if isinstance(value, str):
        try:
            value = value[:21]
        except ValueError:
            logger.exception('Invalid datetime format')
    return value


class CreatedMixin(CustomBaseModel):
    """CreatedMixin"""

    created_at: datetime | str = Field(default=datetime.now())

    @model_validator(mode='before')
    def parse_datetime(self) -> Any:
        """Parse datetime"""
        mydict = dict(self)
        mydict['created_at'] = validate_date(mydict['created_at'])
        return mydict


class TimeStampedMixin(CreatedMixin):
    """TimeStampedMixin"""

    updated_at: datetime | str = Field(default=datetime.now())

    @model_validator(mode='before')
    def parse_datetime(self) -> Any:
        """Parse datetime"""
        mydict = dict(self)
        mydict['created_at'] = validate_date(mydict['created_at'])
        mydict['updated_at'] = validate_date(mydict['updated_at'])
        return mydict


class Genre(UUIDMixin, TimeStampedMixin):
    """Genre"""

    name: str | None = Field(default=None)
    description: str | None = Field(default=None)


class Person(UUIDMixin, TimeStampedMixin):
    """Person"""

    full_name: str | None = Field(default=None)


class FilmWork(UUIDMixin, TimeStampedMixin):
    """FilmWork"""

    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    creation_date: datetime | None = Field(default=None)
    file_path: str | None = Field(default=None)
    rating: float | None = Field(default=None)
    type: str | None = Field(default=None)


class GenreFilmWork(UUIDMixin, CreatedMixin):
    """GenreFilmWork"""

    genre_id: UUID | None = Field(default=None)
    film_work_id: UUID | None = Field(default=None)


class PersonFilmWork(UUIDMixin, CreatedMixin):
    """PersonFilmWork"""

    film_work_id: UUID | None = Field(default=None)
    person_id: UUID | None = Field(default=None)
    role: str | None = Field(default=None)


class PGExecuteData(BaseModel):
    """Class for PG Execute Function"""

    query: str | Any  # here should be LiteralString from typing_extensions
    multi: bool = True
    is_result: bool = True
    data: list = []
