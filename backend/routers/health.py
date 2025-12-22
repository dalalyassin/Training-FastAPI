from fastapi import APIRouter, Depends, Request
from backend.core.security import verify_api_key, get_current_user
from backend.core.rate_limit import limiter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
@limiter.limit("10/minute")  # limit 10 requests per minute
def health_check(
    request: Request,
    _: None = Depends(verify_api_key),
    __: str = Depends(get_current_user)  # optional: enforce OAuth too
):
    return {
        "status": "ok",
        "service": "backend-api"
    }
