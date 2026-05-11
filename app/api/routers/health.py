from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=[""])


@router.get("/health")
def get_health():
    return {"success": True}
