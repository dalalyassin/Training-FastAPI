from fastapi import APIRouter, Depends, Request
from core.rate_limit import limiter
from core.security import verify_api_key

router = APIRouter(prefix="/api-key", tags=["API Key Auth"])


@router.get("/protected")
@limiter.limit("5/minute")
def protected_endpoint(request: Request, _: None = Depends(verify_api_key)):
    return {"message": "You accessed a protected endpoint"}
