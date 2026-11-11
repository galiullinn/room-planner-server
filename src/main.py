from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.exceptions import register_exception_handlers
from src.modules.catalog.routers import category_router

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    debug=settings.app_debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.cors_origins,
    allow_headers=["*"],
    allow_methods=["*"],
)

register_exception_handlers(app)

app.include_router(category_router, prefix=settings.api_prefix)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_title}
