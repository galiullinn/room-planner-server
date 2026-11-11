from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class IntPkMixin:
    """Миксин для добавления первичного ключа типа int."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UuidPkMixin:
    """Миксин для добавления первичного ключа типа UUID."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class TimestampMixin:
    """Миксин для добавления меток времени создания и обновления записи."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
