from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.modules.catalog.repositories import CategoryRepository
from src.modules.catalog.services import CategoryService


def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryRepository:
    return CategoryRepository(session=session)


def get_category_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    repository: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> CategoryService:
    return CategoryService(
        session=session,
        repository=repository,
    )


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
