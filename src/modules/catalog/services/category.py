from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.catalog.exceptions import (
    CategoryHasChildrenError,
    CategoryHasItemsError,
    CategoryNotFoundError,
    CategorySelfReferenceError,
    CategorySlugAlreadyExistsError,
)
from src.modules.catalog.models import Category
from src.modules.catalog.repositories import CategoryRepository
from src.modules.catalog.schemas import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    """Сервис для работы с категориями."""

    def __init__(
        self,
        session: AsyncSession,
        repository: CategoryRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def get_by_id(self, category_id: int) -> Category:
        """Получить категорию по id."""
        category = await self._repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        return category

    async def get_list(
        self,
        *,
        parent_id: int | None = None,
        only_active: bool = False,
    ) -> Sequence[Category]:
        """Получить список категорий."""
        return await self._repository.get_list(
            parent_id=parent_id,
            only_active=only_active,
        )

    async def create(self, data: CategoryCreateSchema) -> Category:
        """Создать новую категорию."""
        if await self._repository.get_by_slug(data.slug) is not None:
            raise CategorySlugAlreadyExistsError()

        if data.parent_id is not None:
            parent = await self._repository.get_by_id(data.parent_id)
            if parent is None or not parent.is_active:
                raise CategoryNotFoundError()

        category = Category(**data.model_dump())
        await self._repository.create(category)
        await self._session.commit()
        return category

    async def update(self, category_id: int, data: CategoryUpdateSchema) -> Category:
        """Обновить данные категории."""
        category = await self.get_by_id(category_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return category

        new_slug = update_data.get("slug")
        if new_slug is not None and new_slug != category.slug:
            if await self._repository.get_by_slug(new_slug) is not None:
                raise CategorySlugAlreadyExistsError()

        new_parent_id = update_data.get("parent_id")
        if new_parent_id is not None and new_parent_id != category.parent_id:
            if new_parent_id == category_id:
                raise CategorySelfReferenceError()
            parent = await self._repository.get_by_id(new_parent_id)
            if parent is None or not parent.is_active:
                raise CategoryNotFoundError()

        await self._repository.update(category, update_data)
        await self._session.commit()
        return category

    async def delete(self, category_id: int) -> None:
        """Удалить категорию."""
        category = await self.get_by_id(category_id)
        if await self._repository.has_children(category_id):
            raise CategoryHasChildrenError()
        if await self._repository.has_items(category_id):
            raise CategoryHasItemsError()
        await self._repository.delete(category)
        await self._session.commit()

    async def deactivate(self, category_id: int) -> Category:
        """Деактивировать категорию (мягкое удаление)."""
        category = await self.get_by_id(category_id)
        if category.is_active:
            await self._repository.update(category, {"is_active": False})
            await self._session.commit()
        return category

    async def restore(self, category_id: int) -> Category:
        """Восстановить категорию."""
        category = await self.get_by_id(category_id)
        if not category.is_active:
            await self._repository.update(category, {"is_active": True})
            await self._session.commit()
        return category
