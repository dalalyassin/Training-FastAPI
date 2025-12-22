from fastapi import APIRouter

router = APIRouter()

@router.get("/public")
def public_endpoint():
    return {"message": "This endpoint is public"}