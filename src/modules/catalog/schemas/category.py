from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreateSchema(BaseModel):
    """Схема создания новой категории."""

    name: str = Field(..., min_length=3, max_length=100, description="Наименование")
    slug: str = Field(..., min_length=3, max_length=100, description="slug")
    sort_order: int = Field(0, description="Приоритет сортировки")
    parent_id: int | None = Field(None, description="Ссылка на родительскую категорию")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class CategoryUpdateSchema(BaseModel):
    """Схема обновления данных категории."""

    name: str | None = Field(None, min_length=3, max_length=100, description="Наименование")
    slug: str | None = Field(None, min_length=3, max_length=100, description="slug")
    sort_order: int | None = Field(None, description="Порядок сортировки")
    parent_id: int | None = Field(None, description="Ссылка на родительскую категорию")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("name", "slug", "sort_order")
    @classmethod
    def check_null(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("Поле не может быть null")
        return value


class CategoryResponseSchema(BaseModel):
    """Схема ответа с данными категории."""

    id: int
    name: str
    slug: str
    is_active: bool
    sort_order: int
    parent_id: int | None

    model_config = ConfigDict(
        from_attributes=True,
    )
