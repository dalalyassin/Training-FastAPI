from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from slowapi.errors import RateLimitExceeded
from backend.routers import public, api_key_auth, oauth, health, chat
from backend.core.rate_limit import limiter

app = FastAPI(title="Backend API")

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(public.router)
app.include_router(api_key_auth.router)
app.include_router(oauth.router)


if __name__ == "__main__":
 uvicorn.run(app, host="0.0.0.0", port=8000)