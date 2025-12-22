from fastapi import APIRouter, Depends, Request
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.core.rate_limit import limiter
from backend.core.security import verify_api_key, get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/message", response_model=ChatResponse)
@limiter.limit("5/minute")  
def chat_message(
    request: ChatRequest,
    _: None = Depends(verify_api_key),
    __: str = Depends(get_current_user)
):
    # For now, dummy reply logic
    last_user_message = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        "Hello"
    )

    reply_text = f"Echo: {last_user_message}"

    return ChatResponse(reply=reply_text)
