from fastapi import FastAPI
import uvicorn
from app.api.routers.auth import router as auth_router
from app.api.routers.health import router as health_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
