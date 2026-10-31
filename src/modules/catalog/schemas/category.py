from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateSchema(BaseModel):
    """Схема создания новой категории."""

    name: str = Field(min_length=1, max_length=200)
    sort_order: int = Field(default=0, ge=0)

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class CategoryUpdateSchema(BaseModel):
    """Схема обновления данных категории."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    sort_order: int | None = Field(default=None, ge=0)

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class CategoryResponseSchema(BaseModel):
    """Схема ответа с данными категории."""

    id: int
    name: str
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
