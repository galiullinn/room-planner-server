from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, UuidPkMixin

if TYPE_CHECKING:
    from .category import Category


class FurnitureItem(UuidPkMixin, Base):
    """Модель предмета мебели."""

    __tablename__ = "furniture_items"

    name: Mapped[str] = mapped_column(String(256))
    slug: Mapped[str] = mapped_column(String(256), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        index=True,
    )

    width_mm: Mapped[int]
    depth_mm: Mapped[int]
    height_mm: Mapped[int]

    is_active: Mapped[bool] = mapped_column(default=True)

    category: Mapped["Category"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<FurnitureItem(id={self.id}, name={self.name!r})>"
