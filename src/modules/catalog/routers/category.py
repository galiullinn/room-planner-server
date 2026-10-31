from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.modules.catalog.models import Category
from src.modules.catalog.schemas import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CategoryUpdateSchema,
)
from src.modules.catalog.services import CategoryService


def get_category_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryService:
    return CategoryService(session)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

router = APIRouter(prefix="/category", tags=["Категории"])


@router.get(
    "",
    response_model=list[CategoryResponseSchema],
    summary="Получить список категорий",
)
async def get_categories(
    service: CategoryServiceDep,
    only_active: bool = False,
) -> Sequence[Category]:
    return await service.get_all(only_active=only_active)


@router.get(
    "/{category_id}",
    response_model=CategoryResponseSchema,
    summary="Получить категорию по id",
)
async def get_category(
    service: CategoryServiceDep,
    category_id: int,
) -> Category:
    return await service.get_by_id(category_id)


@router.post(
    "",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую категорию",
)
async def create_category(
    service: CategoryServiceDep,
    data: CategoryCreateSchema,
) -> Category:
    return await service.create(data)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponseSchema,
    summary="Обновить данные категории",
)
async def update_category(
    service: CategoryServiceDep,
    category_id: int,
    data: CategoryUpdateSchema,
) -> Category:
    return await service.update(category_id, data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    service: CategoryServiceDep,
    category_id: int,
) -> None:
    await service.delete(category_id)
