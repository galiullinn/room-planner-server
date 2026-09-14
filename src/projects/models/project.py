from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, TimestampMixin, UuidPkMixin

if TYPE_CHECKING:
    from src.users.models import User

    from .scene import Scene


class Project(UuidPkMixin, TimestampMixin, Base):
    """Модель проекта."""

    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_published: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    user: Mapped["User"] = relationship(back_populates="projects")
    scene: Mapped["Scene"] = relationship(
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, title={self.title!r})>"
