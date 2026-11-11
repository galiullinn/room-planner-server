from src.core.exceptions import ConflictError, NotFoundError


class FurnitureItemNotFoundError(NotFoundError):
    """Предмет мебели не найден."""

    default_message = "Предмет мебели не найден."


class FurnitureItemAlreadyExistsError(ConflictError):
    """Предмет мебели с указанным slug уже существует."""

    default_message = "Предмет мебели с указанным slug уже существует."
