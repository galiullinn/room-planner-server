from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, TimestampMixin, UuidPkMixin

if TYPE_CHECKING:
    from .project import Project


class Scene(UuidPkMixin, TimestampMixin, Base):
    """Модель сцены проекта."""

    __tablename__ = "scenes"

    scene_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
    )

    project: Mapped["Project"] = relationship(back_populates="scene")

    def __repr__(self) -> str:
        return f"<Scene(id={self.id}, project_id: {self.project_id})>"
