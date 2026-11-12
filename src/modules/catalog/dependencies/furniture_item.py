from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.modules.catalog.repositories import CategoryRepository, FurnitureItemRepository
from src.modules.catalog.services import FurnitureItemService

from .category import get_category_repository


def get_furniture_item_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FurnitureItemRepository:
    return FurnitureItemRepository(session=session)


def get_furniture_item_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    item_repository: Annotated[FurnitureItemRepository, Depends(get_furniture_item_repository)],
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> FurnitureItemService:
    return FurnitureItemService(
        session=session,
        item_repository=item_repository,
        category_repository=category_repository,
    )


FurnitureItemServiceDep = Annotated[FurnitureItemService, Depends(get_furniture_item_service)]
