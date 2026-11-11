from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, IntPkMixin


class Category(IntPkMixin, Base):
    """Модель категории предметов мебели."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        index=True,
    )

    parent: Mapped["Category | None"] = relationship(
        back_populates="children",
        remote_side="Category.id",
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent",
        passive_deletes="all",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name!r})>"
