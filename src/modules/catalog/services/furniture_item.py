from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.catalog.exceptions import (
    CategoryNotFoundError,
    FurnitureItemAlreadyExistsError,
    FurnitureItemNotFoundError,
)
from src.modules.catalog.models import FurnitureItem
from src.modules.catalog.repositories import CategoryRepository, FurnitureItemRepository
from src.modules.catalog.schemas import FurnitureItemCreateSchema, FurnitureItemUpdateSchema


class FurnitureItemService:
    """Сервис для работы с предметами мебели."""

    def __init__(
        self,
        session: AsyncSession,
        item_repository: FurnitureItemRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._session = session
        self._item_repository = item_repository
        self._category_repository = category_repository

    async def get_by_id(self, item_id: UUID) -> FurnitureItem:
        """Получить предмет мебели по id."""
        item = await self._item_repository.get_by_id(item_id)
        if item is None:
            raise FurnitureItemNotFoundError()
        return item

    async def get_list(
        self,
        *,
        category_id: int | None = None,
        only_active: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[FurnitureItem]:
        """Получить список предметов мебели."""
        return await self._item_repository.get_list(
            category_id=category_id,
            only_active=only_active,
            limit=limit,
            offset=offset,
        )

    async def create(self, data: FurnitureItemCreateSchema) -> FurnitureItem:
        """Создать новый предмет мебели."""
        if await self._item_repository.get_by_slug(data.slug) is not None:
            raise FurnitureItemAlreadyExistsError()

        if await self._category_repository.get_by_id(data.category_id) is None:
            raise CategoryNotFoundError()

        item = FurnitureItem(**data.model_dump())
        await self._item_repository.create(item)
        await self._session.commit()
        return item

    async def update(self, item_id: UUID, data: FurnitureItemUpdateSchema) -> FurnitureItem:
        """Обновить данные предмета мебели."""
        item = await self.get_by_id(item_id)
        update_data = data.model_dump(exclude_unset=True)

        new_slug = update_data.get("slug")
        if new_slug is not None and new_slug != item.slug:
            if await self._item_repository.get_by_slug(new_slug) is not None:
                raise FurnitureItemAlreadyExistsError()

        new_category_id = update_data.get("category_id")
        if new_category_id is not None:
            if await self._category_repository.get_by_id(new_category_id) is None:
                raise CategoryNotFoundError()

        await self._item_repository.update(item, update_data)
        await self._session.commit()
        return item

    async def delete(self, item_id: UUID) -> None:
        """Удалить предмет мебели."""
        item = await self.get_by_id(item_id)
        await self._item_repository.delete(item)
        await self._session.commit()

    async def deactivate(self, item_id: UUID) -> FurnitureItem:
        """Деактивировать предмет мебели (мягкое удаление)."""
        item = await self.get_by_id(item_id)
        if item.is_active:
            await self._item_repository.update(item, {"is_active": False})
            await self._session.commit()
        return item

    async def restore(self, item_id: UUID) -> FurnitureItem:
        """Восстановить предмет мебели."""
        item = await self.get_by_id(item_id)
        if not item.is_active:
            await self._item_repository.update(item, {"is_active": True})
            await self._session.commit()
        return item
