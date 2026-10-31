from typing import ClassVar

from src.core.exceptions import ConflictError, NotFoundError


class CategoryNotFoundError(NotFoundError):
    """Категорий не найдена."""

    default_message: ClassVar[str] = "Категория не найдена."


class CategoryAlreadyExistsError(ConflictError):
    """Категория с таким названием уже существует."""

    default_message: ClassVar[str] = "Категория с таким названием уже существует."
