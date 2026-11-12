from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    url=settings.db_url,
    echo=settings.db_echo,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Получить асинхронную сессию для работы с базой данных."""
    async with async_session_maker() as session:
        yield session
