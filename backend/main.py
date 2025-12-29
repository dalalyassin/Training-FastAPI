import uuid

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from core.rate_limit import limiter
from routers import api_key_auth, chat, health, oauth, public

app = FastAPI(title="Backend API")

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(public.router)
app.include_router(api_key_auth.router)
app.include_router(oauth.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
