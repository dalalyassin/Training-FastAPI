from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    text: str
    content: str


class Prompt(BaseModel):
    text: str
    user_id: int | None = None
    metadata: dict[str, Any] | None = None
    talk: int


class LLMResponse(BaseModel):
    prompt: Prompt
    response_text: str
    tokens_used: int
