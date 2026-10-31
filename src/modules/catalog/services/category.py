from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.catalog.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError
from src.modules.catalog.models import Category
from src.modules.catalog.repositories import CategoryRepository
from src.modules.catalog.schemas import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    """Сервис для работы с категориями предметов мебели."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = CategoryRepository(session)

    async def get_by_id(self, category_id: int) -> Category:
        """Получить категорию по id."""
        category = await self._repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        return category

    async def get_all(self, *, only_active: bool = False) -> Sequence[Category]:
        """Получить список категорий."""
        return await self._repository.get_all(only_active=only_active)

    async def create(self, data: CategoryCreateSchema) -> Category:
        """Создать новую категорию."""
        if await self._repository.get_by_name(data.name) is not None:
            raise CategoryAlreadyExistsError()
        category = Category(**data.model_dump())
        await self._repository.create(category)
        await self._session.commit()
        return category

    async def update(self, category_id: int, data: CategoryUpdateSchema) -> Category:
        """Обновить данные категории."""
        category = await self.get_by_id(category_id)
        updated_category = data.model_dump(exclude_unset=True)

        if not updated_category:
            return category

        new_name = updated_category.get("name")
        if new_name is not None and new_name != category.name:
            if await self._repository.get_by_name(new_name) is not None:
                raise CategoryAlreadyExistsError()

        await self._repository.update(category, updated_category)
        await self._session.commit()
        return category

    async def delete(self, category_id: int) -> None:
        """Удалить категорию."""
        category = await self.get_by_id(category_id)
        await self._repository.delete(category)
        await self._session.commit()
