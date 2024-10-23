from uuid import UUID, uuid4

import names
from pydantic import Field

from src.schemas.custom_base_model import CustomBaseModel


class UsersId(CustomBaseModel):
    """UsersId"""

    id: UUID = Field(default=uuid4())


class Users(UsersId):
    """Users"""

    name: str = Field(default=names.get_full_name())
