from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    text: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


# Add these new schemas
class Prompt(BaseModel):
    text: str


class LLMResponse(BaseModel):
    response_text: str
    tokens_used: int
