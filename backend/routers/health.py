from fastapi import APIRouter, Depends, Request
from core.security import verify_api_key
from core.rate_limit import limiter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
@limiter.limit("10/minute")
def health_check(
    request: Request,
    _: None = Depends(verify_api_key),
    # __: str = Depends(get_current_user)
):
    request_id = request.state.request_id
    print(f"Request ID: {request_id}")
    return {"status": "ok", "service": "backend-api", "request_id": request_id}
