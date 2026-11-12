from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.catalog.models import FurnitureItem


class FurnitureItemRepository:
    """Репозиторий для работы с предметами мебели."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, item_id: UUID) -> FurnitureItem | None:
        """Получить предмет мебели по id."""
        return await self._session.get(FurnitureItem, item_id)

    async def get_by_slug(self, slug: str) -> FurnitureItem | None:
        """Получить предмет мебели по slug."""
        stmt = select(FurnitureItem).where(FurnitureItem.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(
        self,
        *,
        category_id: int | None = None,
        only_active: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[FurnitureItem]:
        """Получить список предметов мебели."""
        stmt = select(FurnitureItem).order_by(FurnitureItem.name)
        if category_id is not None:
            stmt = stmt.where(FurnitureItem.category_id == category_id)
        if only_active:
            stmt = stmt.where(FurnitureItem.is_active.is_(True))
        stmt = stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, item: FurnitureItem) -> None:
        """Создать новый предмет мебели."""
        self._session.add(item)
        await self._session.flush()

    async def update(self, item: FurnitureItem, data: dict[str, Any]) -> None:
        """Обновить данные предмета мебели."""
        for field, value in data.items():
            setattr(item, field, value)
        await self._session.flush()

    async def delete(self, item: FurnitureItem) -> None:
        """Удалить предмет мебели."""
        await self._session.delete(item)
        await self._session.flush()
