from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FurnitureItemCreateSchema(BaseModel):
    """Схема создания нового предмета мебели."""

    name: str = Field(..., min_length=3, max_length=256, description="Наименование")
    slug: str = Field(..., min_length=3, max_length=256, description="slug")
    description: str | None = Field(None, description="Описание")
    category_id: int = Field(..., description="Категория предмета")
    width_mm: int = Field(gt=0, le=10000, description="Ширина, мм")
    depth_mm: int = Field(gt=0, le=10000, description="Глубина, мм")
    height_mm: int = Field(gt=0, le=10000, description="Высота, мм")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class FurnitureItemUpdateSchema(BaseModel):
    """Схема обновления данных предмета мебели."""

    name: str = Field(..., min_length=3, max_length=256, description="Наименование")
    slug: str = Field(..., min_length=3, max_length=256, description="slug")
    description: str | None = Field(None, description="Описание")
    category_id: int = Field(..., description="Категория предмета")
    width_mm: int = Field(gt=0, le=10000, description="Ширина, мм")
    depth_mm: int = Field(gt=0, le=10000, description="Глубина, мм")
    height_mm: int = Field(gt=0, le=10000, description="Высота, мм")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class FurnitureItemResponseSchema(BaseModel):
    """Схема ответа с данными предмета мебели."""

    id: UUID
    name: str
    slug: str
    description: str | None
    category_id: int
    width_mm: int
    depth_mm: int
    height_mm: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
