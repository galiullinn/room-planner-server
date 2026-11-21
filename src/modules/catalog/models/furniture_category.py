from sqlalchemy import CheckConstraint, ForeignKey, String, text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, IntPkMixin


class FurnitureCategory(IntPkMixin, Base):
    """Модель категории предметов мебели."""

    __tablename__ = "furniture_categories"
    __table_args__ = (
        CheckConstraint("id != parent_id", name="no_self_reference"),
        CheckConstraint("sort_order >= 0", name="sort_order_positive"),
    )

    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    sort_order: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("furniture_categories.id", ondelete="RESTRICT"),
        index=True,
    )

    parent: Mapped["FurnitureCategory | None"] = relationship(
        back_populates="children",
        remote_side="FurnitureCategory.id",
    )
    children: Mapped[list["FurnitureCategory"]] = relationship(
        back_populates="parent",
        order_by="FurnitureCategory.sort_order",
        passive_deletes="all",
    )

    def __repr__(self) -> str:
        return f"<FurnitureCategory(id={self.id}, slug={self.slug!r})>"
