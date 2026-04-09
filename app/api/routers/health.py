from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/health")
def get_health():
    return {"succeess": True}
