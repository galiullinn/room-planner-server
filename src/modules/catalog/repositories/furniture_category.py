from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.catalog.models import FurnitureCategory


class FurnitureCategoryRepository:
    """Репозиторий для работы с категориями предметов мебели."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        category_id: int,
        *,
        with_children: bool = False,
    ) -> FurnitureCategory | None:
        """Получить категорию по id."""
        stmt = select(FurnitureCategory).where(FurnitureCategory.id == category_id)
        if with_children:
            stmt = stmt.options(selectinload(FurnitureCategory.children))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> FurnitureCategory | None:
        """Получить категорию по slug."""
        stmt = select(FurnitureCategory).where(FurnitureCategory.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list(self, *, only_active: bool = False) -> list[FurnitureCategory]:
        """Получить список всех категорий."""
        stmt = select(FurnitureCategory).order_by(
            FurnitureCategory.sort_order,
            FurnitureCategory.id,
        )
        if only_active:
            stmt = stmt.where(FurnitureCategory.is_active.is_(True))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_roots(self, *, only_active: bool = False) -> list[FurnitureCategory]:
        """Получить список корневых категорий."""
        stmt = (
            select(FurnitureCategory)
            .where(FurnitureCategory.parent_id.is_(None))
            .order_by(FurnitureCategory.sort_order, FurnitureCategory.id)
        )
        if only_active:
            stmt = stmt.where(FurnitureCategory.is_active.is_(True))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_children(
        self,
        parent_id: int,
        *,
        only_active: bool = False,
    ) -> list[FurnitureCategory]:
        """Получить список дочерних категорий родителя."""
        stmt = (
            select(FurnitureCategory)
            .where(FurnitureCategory.parent_id == parent_id)
            .order_by(FurnitureCategory.sort_order, FurnitureCategory.id)
        )
        if only_active:
            stmt = stmt.where(FurnitureCategory.is_active.is_(True))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def exists_by_slug(self, slug: str) -> bool:
        """Проверить занятость slug."""
        stmt = select(FurnitureCategory.id).where(FurnitureCategory.slug == slug).limit(1)
        result = await self._session.execute(stmt)
        return result.first() is not None

    async def has_children(self, category_id: int) -> bool:
        """Проверить наличие дочерних категорий."""
        stmt = (
            select(FurnitureCategory.id).where(FurnitureCategory.parent_id == category_id).limit(1)
        )
        result = await self._session.execute(stmt)
        return result.first() is not None

    async def create(self, category: FurnitureCategory) -> None:
        """Создать новую категорию."""
        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)

    async def update(self, category: FurnitureCategory, data: dict[str, Any]) -> None:
        """ "Обновить данные категории."""
        for field, value in data.items():
            setattr(category, field, value)
        await self._session.flush()
        await self._session.refresh(category)

    async def delete(self, category: FurnitureCategory) -> None:
        """Удалить категорию."""
        await self._session.delete(category)
        await self._session.flush()
