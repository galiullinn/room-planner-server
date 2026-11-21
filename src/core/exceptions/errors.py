from typing import ClassVar


class AppError(Exception):
    """Базовое исключение приложения."""

    status_code: ClassVar[int] = 500
    error_code: ClassVar[str] = "internal_error"
    default_message: ClassVar[str] = "Внутренняя ошибка приложения."

    def __init__(self, message: str | None = None) -> None:
        self.message: str = message or self.default_message
        super().__init__(self.message)


class BadRequestError(AppError):
    """Некорректный запрос."""

    status_code = 400
    error_code = "bad_request"
    default_message = "Некорректный запрос."


class NotFoundError(AppError):
    """Запрашиваемый ресурс не найден."""

    status_code = 404
    error_code = "not_found"
    default_message = "Запрашиваемый ресурс не найден."


class ConflictError(AppError):
    """Конфликт с текущим состоянием ресурса."""

    status_code = 409
    error_code = "conflict"
    default_message = "Конфликт с текущим состоянием ресурса."
