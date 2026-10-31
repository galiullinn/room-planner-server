from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.catalog.models import Category


class CategoryRepository:
    """Репозиторий для работы с категориями предметов мебели."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        """Получить категорию по id."""
        return await self._session.get(Category, category_id)

    async def get_by_name(self, name: str) -> Category | None:
        """Получить категорию по name."""
        stmt = select(Category).where(Category.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, *, only_active: bool = False) -> Sequence[Category]:
        """Получить список категорий."""
        stmt = select(Category).order_by(Category.sort_order, Category.name)
        if only_active:
            stmt = stmt.where(Category.is_active.is_(True))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, category: Category) -> Category:
        """Создать новую категорию."""
        self._session.add(category)
        await self._session.flush()
        return category

    async def update(self, category: Category, data: dict[str, Any]) -> Category:
        """Обновить данные категории."""
        for field, value in data.items():
            setattr(category, field, value)
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        """Удалить категорию."""
        await self._session.delete(category)
        await self._session.flush()
