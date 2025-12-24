from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from schemas.chat import Prompt
from services.llm import generate_stream_response
from core.security import verify_api_key
from core.rate_limit import limiter

router = APIRouter()


@router.post("/message/stream")
@limiter.limit("5/minute")
async def chat_message_stream(
    request: Request,
    prompt: Prompt,
    _: None = Depends(verify_api_key),
    # __: str = Depends(get_current_user),
):
    request_id = request.state.request_id
    print(f"Request ID: {request_id}")

    return StreamingResponse(
        generate_stream_response(prompt),
        media_type="text/plain",
    )


# @router.post("/message", response_model=ChatResponse)
# @limiter.limit("5/minute")
# def chat_message(
#     request: ChatRequest,
#     _: None = Depends(verify_api_key),
#     __: str = Depends(get_current_user)
# ):
#     last_user_message = next(
#         (m.content for m in reversed(request.messages) if m.role == "user"),
#         "Hello"
#     )

#     reply_text = f"Echo: {last_user_message}"

#     return ChatResponse(reply=reply_text)
