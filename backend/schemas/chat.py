from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    text: str 
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    

class ChatResponse(BaseModel):
    reply: str

