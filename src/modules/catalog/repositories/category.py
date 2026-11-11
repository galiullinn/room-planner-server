from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.catalog.models import Category, FurnitureItem


class CategoryRepository:
    """Репозиторий для работы с категориями предметов мебели."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        """Получить категорию по id."""
        return await self._session.get(Category, category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        """Получить категорию по slug."""
        stmt = select(Category).where(Category.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(
        self,
        *,
        parent_id: int | None = None,
        only_active: bool = False,
    ) -> Sequence[Category]:
        """Получить список категорий."""
        stmt = select(Category).order_by(Category.sort_order, Category.name)
        if parent_id is not None:
            stmt = stmt.where(Category.parent_id == parent_id)
        if only_active:
            stmt = stmt.where(Category.is_active.is_(True))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, category: Category) -> None:
        """Создать новую категорию."""
        self._session.add(category)
        await self._session.flush()

    async def update(self, category: Category, data: dict[str, Any]) -> None:
        """Обновить данные категории."""
        for field, value in data.items():
            setattr(category, field, value)
        await self._session.flush()

    async def delete(self, category: Category) -> None:
        """Удалить категорию."""
        await self._session.delete(category)
        await self._session.flush()

    async def has_children(self, category_id: int) -> bool:
        """Выполнить проверку наличия дочерних категорий."""
        stmt = select(Category.id).where(Category.parent_id == category_id).limit(1)
        result = await self._session.execute(stmt)
        return result.first() is not None

    async def has_items(self, category_id: int) -> bool:
        """Выполнить проверку наличия предметов в категории."""
        stmt = select(FurnitureItem.id).where(FurnitureItem.category_id == category_id).limit(1)
        result = await self._session.execute(stmt)
        return result.first() is not None
