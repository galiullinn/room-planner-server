from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UuidPkMixin:
    """Миксин для добавления первичного ключа типа UUID."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class IntPkMixin:
    """Миксин для добавления первичного ключа типа int."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin:
    """Миксин для добавления меток времени создания и обновления записи."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
