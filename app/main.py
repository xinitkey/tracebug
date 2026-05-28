from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

from app.api.routers.auth import router as auth_router
from app.api.routers.health import router as health_router
from app.api.routers.task import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
