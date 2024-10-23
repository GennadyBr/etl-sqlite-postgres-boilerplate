""" Messages """
from enum import StrEnum


class ErrorMessages(StrEnum):
    """Messages"""

    ERROR = 'error'
    AttribError = 'Attribute error '
    ConError = 'Connection error '
    TypError = 'Type error '

    TableDoesNotExist = 'Table does not exist'
    IDNotValid = 'ID is not valid'
    OperationalError = 'Operational error'
    ProgrammingError = 'Programming error'
    UniqueViolation = 'Unique violation'
    ForeignKeyViolation = 'Foreign key violation'
    InvalidDatetimeFormat = 'Invalid datetime format'
