
from pydantic import BaseModel, Field, HttpUrl


class ChatRequest(BaseModel):
    repository_url: HttpUrl
    question: str = Field(..., min_length=1, max_length=5000)
    session_id: str = Field(..., min_length=1, max_length=128)


class ChatResponse(BaseModel):
    status: str
    session_id: str
    question: str
    answer: str
    citations: list = Field(default_factory=list)
    conversation_size: int
