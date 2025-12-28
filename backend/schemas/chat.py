from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    text: str
    content: str


class Prompt(BaseModel):
    text: str
    user_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    talk: int


class LLMResponse(BaseModel):
    prompt: Prompt
    response_text: str
    tokens_used: int
