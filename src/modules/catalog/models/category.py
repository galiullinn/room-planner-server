from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base, IntPkMixin, TimestampMixin


class Category(IntPkMixin, TimestampMixin, Base):
    """Модель категорий предметов мебели."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(200), unique=True)
    sort_order: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name!r})>"
