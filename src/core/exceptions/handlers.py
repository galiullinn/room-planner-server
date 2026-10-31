from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .errors import AppError


def register_exception_handlers(app: FastAPI) -> None:
    """Зарегистрировать обработчики исключений приложения."""

    @app.exception_handler(AppError)
    async def app_exception_handler(
        request: Request,
        exc: AppError,
    ) -> JSONResponse:
        """Обработать ошибки приложения."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Обработать ошибки валидации входных данных."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": "Невалидные данные"},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Обработать непредвиденные исключения."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Внутренняя ошибка приложения"},
        )
