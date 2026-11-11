from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column


class IntPkMixin:
    """Миксин для добавления первичного ключа типа int."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UuidPkMixin:
    """Миксин для добавления первичного ключа типа UUID."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
