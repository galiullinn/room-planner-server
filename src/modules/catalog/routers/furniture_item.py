from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status
from src.modules.catalog.dependencies import FurnitureItemServiceDep
from src.modules.catalog.models import FurnitureItem
from src.modules.catalog.schemas import (
    FurnitureItemCreateSchema,
    FurnitureItemResponseSchema,
    FurnitureItemUpdateSchema,
)

router = APIRouter(prefix="/furniture", tags=["Предметы мебели"])


@router.get(
    "",
    response_model=list[FurnitureItemResponseSchema],
    summary="Получить список предметов мебели",
)
async def get_furniture(
    service: FurnitureItemServiceDep,
    category_id: int | None = None,
    only_active: bool = False,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Sequence[FurnitureItem]:
    return await service.get_list(
        category_id=category_id,
        only_active=only_active,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{item_id}",
    response_model=FurnitureItemResponseSchema,
    summary="Получить предмет мебели по id",
)
async def get_furniture_item(
    service: FurnitureItemServiceDep,
    item_id: UUID,
) -> FurnitureItem:
    return await service.get_by_id(item_id)


@router.post(
    "",
    response_model=FurnitureItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый предмет мебели",
)
async def create_furniture(
    service: FurnitureItemServiceDep,
    data: FurnitureItemCreateSchema,
) -> FurnitureItem:
    return await service.create(data)


@router.put(
    "/{item_id}",
    response_model=FurnitureItemResponseSchema,
    summary="Обновить данные предмета мебели",
)
async def update_furniture(
    service: FurnitureItemServiceDep,
    item_id: UUID,
    data: FurnitureItemUpdateSchema,
) -> FurnitureItem:
    return await service.update(item_id, data)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить предмет мебели",
)
async def delete_furniture(
    service: FurnitureItemServiceDep,
    item_id: UUID,
) -> None:
    await service.delete(item_id)


@router.post(
    "/{item_id}/deactivate",
    response_model=FurnitureItemResponseSchema,
    summary="Деактивировать предмет мебели",
)
async def deactivate_furniture(
    service: FurnitureItemServiceDep,
    item_id: UUID,
) -> FurnitureItem:
    return await service.deactivate(item_id)


@router.post(
    "/{item_id}/restore",
    response_model=FurnitureItemResponseSchema,
    summary="Восстановить предмет мебели",
)
async def restore_furniture(
    service: FurnitureItemServiceDep,
    item_id: UUID,
) -> FurnitureItem:
    return await service.restore(item_id)
