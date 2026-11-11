from src.core.exceptions import BadRequestError, ConflictError, NotFoundError


class CategoryNotFoundError(NotFoundError):
    """Категория не найдена."""

    default_message = "Категория не найдена."


class CategorySlugAlreadyExistsError(ConflictError):
    """Категория с указанным slug уже существует."""

    default_message = "Категория с указанным slug уже существует."


class CategorySelfReferenceError(BadRequestError):
    """Категория не может ссылаться сама на себя."""

    default_message = "Категория не может ссылаться сама на себя."


class CategoryHasChildrenError(ConflictError):
    """Нельзя удалить категорию, у которой есть дочерние категории."""

    default_message = "Нельзя удалить категорию, у которой есть дочерние категории."


class CategoryHasItemsError(ConflictError):
    """Нельзя удалить категорию, у которой есть предметы мебели."""

    default_message = "Нельзя удалить категорию, у которой есть предметы мебели."
