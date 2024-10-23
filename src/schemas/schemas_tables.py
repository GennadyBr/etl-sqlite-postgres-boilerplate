from pydantic import Field

from src.schemas.custom_base_model import SchemaModel


class UserTables(SchemaModel):
    """UserTables"""

    table_name: str | None = Field(default="None")
