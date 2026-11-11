from typing import ClassVar


class AppError(Exception):
    """Базовое исключение приложения."""

    default_message: ClassVar[str] = "Внутренняя ошибка приложения."
    status_code: ClassVar[int] = 500

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class BadRequestError(AppError):
    """Некорректный запрос."""

    default_message = "Некорректный запрос"
    status_code = 400


class NotFoundError(AppError):
    """Запрашиваемый ресурс не найден."""

    default_message = "Запрашиваемый ресурс не найден."
    status_code = 404


class ConflictError(AppError):
    """Конфликт с текущим состоянием ресурса."""

    default_message = "Конфликт с текущим состоянием ресурса."
    status_code = 409
