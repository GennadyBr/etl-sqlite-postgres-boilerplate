from pydantic import BaseModel, Field


class CustomBaseModel(BaseModel):
    """Custom BaseModel"""

    class Config:
        """Custom Config"""

        from_attributes = True


class SchemaModel(CustomBaseModel):
    """ContentSchema"""

    schema_name: str = Field(default='content')
