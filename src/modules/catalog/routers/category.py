from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Query, status
from src.modules.catalog.dependencies import CategoryServiceDep
from src.modules.catalog.models import Category
from src.modules.catalog.schemas import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CategoryUpdateSchema,
)

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.get(
    "",
    response_model=list[CategoryResponseSchema],
    summary="Получить список категорий",
)
async def get_categories(
    service: CategoryServiceDep,
    parent_id: Annotated[int | None, Query(ge=1)] = None,
    only_active: Annotated[bool, Query()] = False,
) -> Sequence[Category]:
    return await service.get_list(
        parent_id=parent_id,
        only_active=only_active,
    )


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


@router.post(
    "/{category_id}/deactivate",
    response_model=CategoryResponseSchema,
    summary="Деактивировать категорию (мягкое удаление)",
)
async def deactivate_category(
    service: CategoryServiceDep,
    category_id: int,
) -> Category:
    return await service.deactivate(category_id)


@router.post(
    "/{category_id}/restore",
    response_model=CategoryResponseSchema,
    summary="Восстановить категорию",
)
async def restore_category(
    service: CategoryServiceDep,
    category_id: int,
) -> Category:
    return await service.restore(category_id)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    service: CategoryServiceDep,
    category_id: int,
) -> None:
    return await service.delete(category_id)
