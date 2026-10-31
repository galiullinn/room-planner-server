from typing import ClassVar


class AppError(Exception):
    """Базовое исключение."""

    default_message: ClassVar[str] = "Внутренняя ошибка сервера."
    status_code: ClassVar[int] = 500

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(AppError):
    """Запрашиваемый ресурс не найден."""

    default_message: ClassVar[str] = "Запрашиваемый ресурс не найден."
    status_code: ClassVar[int] = 404


class ConflictError(AppError):
    """Конфликт с текущим состоянием ресурса."""

    default_message: ClassVar[str] = "Конфликт с текущим состоянием ресурса."
    status_code: ClassVar[int] = 409
