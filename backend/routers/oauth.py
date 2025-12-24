from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from core.security import create_access_token, get_current_user
from core.rate_limit import limiter
from schemas.auth import Token

router = APIRouter(tags=["OAuth"])


@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": form_data.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/oauth-protected")
@limiter.limit("10/minute")
def oauth_protected(request: Request, user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, rate-limited & authenticated"}
